"""
Analysis API Endpoints

This module contains the core API endpoints for analyzing products.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import asyncio
from datetime import datetime
import logging

from app.core.database import get_db
from app.models.database_models import (
    Product, Analysis, CustomerComment, Topic,
    AnalysisStatus, SentimentType
)
from app.models.schemas import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisJobResponse,
    DashboardData,
    ProductResponse,
    CommentResponse,
    TopicResponse
)
from app.scrapers import create_scraper
from app.ml import get_sentiment_analyzer, get_churn_predictor
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analysis", tags=["analysis"])


async def run_analysis_job(analysis_id: int, product_name: str):
    """
    Background task to run the complete analysis pipeline
    
    Steps:
    1. Scrape customer comments from web
    2. Run sentiment analysis on each comment
    3. Calculate aggregate metrics
    4. Predict churn risk
    5. Extract topics (basic keyword extraction)
    6. Update analysis status
    """
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Update status to in_progress
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return
        
        analysis.status = AnalysisStatus.IN_PROGRESS
        db.commit()
        
        logger.info(f"Starting analysis job {analysis_id} for product: {product_name}")
        
        # Step 1: Scrape data
        scraper = create_scraper(
            user_agent=settings.USER_AGENT,
            timeout=settings.SCRAPE_TIMEOUT
        )
        
        comments = await scraper.scrape_all_sources(
            product_name,
            max_results=settings.MAX_SCRAPE_RESULTS
        )
        
        if not comments:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = "No comments found"
            db.commit()
            return
        
        logger.info(f"Scraped {len(comments)} comments")
        
        # Step 2: Sentiment analysis
        sentiment_analyzer = get_sentiment_analyzer()
        texts = [c.text for c in comments]
        sentiments = sentiment_analyzer.analyze_batch(texts)
        
        # Step 3: Save comments to database
        comment_objects = []
        sentiment_scores = []
        
        for comment, sentiment in zip(comments, sentiments):
            # Map sentiment string to enum
            sentiment_type = SentimentType(sentiment['sentiment'])
            
            db_comment = CustomerComment(
                product_id=analysis.product_id,
                analysis_id=analysis_id,
                text=comment.text,
                source=comment.source,
                source_url=comment.source_url,
                author=comment.author,
                sentiment=sentiment_type,
                sentiment_score=sentiment['score'],
                confidence=sentiment['confidence'],
                posted_at=comment.posted_at
            )
            
            comment_objects.append(db_comment)
            sentiment_scores.append(sentiment['score'])
        
        db.add_all(comment_objects)
        db.commit()
        
        # Step 4: Calculate aggregate metrics
        total = len(comments)
        positive = sum(1 for s in sentiments if s['sentiment'] == 'positive')
        negative = sum(1 for s in sentiments if s['sentiment'] == 'negative')
        neutral = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        # Step 5: Predict churn risk
        churn_predictor = get_churn_predictor()
        
        negative_ratio = negative / total if total > 0 else 0
        sentiment_volatility = sum(abs(s - avg_sentiment) for s in sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        churn_result = churn_predictor.predict_churn_from_sentiment(
            avg_sentiment=avg_sentiment,
            negative_ratio=negative_ratio,
            total_comments=total,
            sentiment_volatility=sentiment_volatility
        )
        
        # Step 6: Extract topics (simple keyword extraction)
        topics = extract_topics(texts, sentiments)
        
        topic_objects = []
        for topic_name, topic_data in topics.items():
            db_topic = Topic(
                analysis_id=analysis_id,
                name=topic_name,
                keywords=", ".join(topic_data['keywords']),
                mention_count=topic_data['count'],
                avg_sentiment=topic_data['avg_sentiment']
            )
            topic_objects.append(db_topic)
        
        db.add_all(topic_objects)
        
        # Step 7: Update analysis with results
        analysis.status = AnalysisStatus.COMPLETED
        analysis.total_comments = total
        analysis.positive_count = positive
        analysis.negative_count = negative
        analysis.neutral_count = neutral
        analysis.avg_sentiment_score = avg_sentiment
        analysis.churn_risk_score = churn_result['churn_probability']
        analysis.completed_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Analysis job {analysis_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error in analysis job {analysis_id}: {e}", exc_info=True)
        
        # Update analysis status to failed
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(e)
            db.commit()
    
    finally:
        db.close()


def extract_topics(texts: List[str], sentiments: List[dict]) -> dict:
    """
    Simple topic extraction based on common keywords
    
    In a production system, you'd use more sophisticated NLP techniques
    like LDA, BERT topic modeling, or keyword extraction algorithms.
    """
    from collections import defaultdict
    import re
    
    # Common topics/themes to look for
    topic_keywords = {
        "price": ["price", "expensive", "cheap", "cost", "pricing", "affordable", "$"],
        "quality": ["quality", "reliable", "durable", "broken", "defective"],
        "support": ["support", "service", "help", "customer service", "response"],
        "features": ["feature", "functionality", "capability", "option", "tool"],
        "performance": ["fast", "slow", "performance", "speed", "lag", "responsive"],
        "usability": ["easy", "difficult", "intuitive", "user-friendly", "complicated"],
    }
    
    topics = defaultdict(lambda: {"count": 0, "keywords": set(), "sentiments": []})
    
    for text, sentiment in zip(texts, sentiments):
        text_lower = text.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics[topic]["count"] += 1
                topics[topic]["sentiments"].append(sentiment['score'])
                
                # Find which keyword matched
                for kw in keywords:
                    if kw in text_lower:
                        topics[topic]["keywords"].add(kw)
    
    # Calculate average sentiment for each topic
    result = {}
    for topic, data in topics.items():
        if data["count"] > 0:
            result[topic] = {
                "count": data["count"],
                "keywords": list(data["keywords"])[:5],  # Top 5 keywords
                "avg_sentiment": sum(data["sentiments"]) / len(data["sentiments"])
            }
    
    return result


@router.post("/analyze", response_model=AnalysisJobResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start a new analysis job for a product
    
    This endpoint:
    1. Creates or finds the product in the database
    2. Creates a new analysis record
    3. Starts background scraping and analysis
    4. Returns immediately with job ID
    """
    try:
        # Find or create product
        product = db.query(Product).filter(Product.name == request.product_name).first()
        
        if not product:
            product = Product(name=request.product_name)
            db.add(product)
            db.commit()
            db.refresh(product)
            logger.info(f"Created new product: {request.product_name}")
        
        # Create new analysis
        analysis = Analysis(
            product_id=product.id,
            status=AnalysisStatus.PENDING
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        # Start background task
        background_tasks.add_task(run_analysis_job, analysis.id, request.product_name)
        
        logger.info(f"Started analysis job {analysis.id}")
        
        return AnalysisJobResponse(
            message=f"Analysis started for '{request.product_name}'",
            analysis_id=analysis.id,
            status=analysis.status,
            estimated_time_seconds=60
        )
        
    except Exception as e:
        logger.error(f"Error starting analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_status(analysis_id: int, db: Session = Depends(get_db)):
    """Get the status of an analysis job"""
    
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis


@router.get("/dashboard/{product_name}", response_model=DashboardData)
def get_dashboard_data(product_name: str, db: Session = Depends(get_db)):
    """
    Get comprehensive dashboard data for a product
    
    Returns latest analysis results, comments, topics, and metrics
    """
    # Find product
    product = db.query(Product).filter(Product.name == product_name).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get latest completed analysis
    latest_analysis = (
        db.query(Analysis)
        .filter(
            Analysis.product_id == product.id,
            Analysis.status == AnalysisStatus.COMPLETED
        )
        .order_by(Analysis.completed_at.desc())
        .first()
    )
    
    if not latest_analysis:
        return DashboardData(
            product=ProductResponse.model_validate(product),
            latest_analysis=None,
            recent_comments=[],
            topics=[],
            sentiment_distribution={},
            sentiment_timeline=[],
            risk_level=None
        )
    
    # Get recent comments
    recent_comments = (
        db.query(CustomerComment)
        .filter(CustomerComment.analysis_id == latest_analysis.id)
        .order_by(CustomerComment.scraped_at.desc())
        .limit(20)
        .all()
    )
    
    # Get topics
    topics = (
        db.query(Topic)
        .filter(Topic.analysis_id == latest_analysis.id)
        .order_by(Topic.mention_count.desc())
        .all()
    )
    
    # Calculate sentiment distribution
    total = latest_analysis.total_comments
    sentiment_dist = {
        "positive": round(latest_analysis.positive_count / total * 100, 1) if total > 0 else 0,
        "negative": round(latest_analysis.negative_count / total * 100, 1) if total > 0 else 0,
        "neutral": round(latest_analysis.neutral_count / total * 100, 1) if total > 0 else 0,
    }
    
    # Determine risk level
    churn_score = latest_analysis.churn_risk_score or 0
    if churn_score < 0.3:
        risk_level = "low"
    elif churn_score < 0.6:
        risk_level = "medium"
    else:
        risk_level = "high"
    
    return DashboardData(
        product=ProductResponse.model_validate(product),
        latest_analysis=AnalysisResponse.model_validate(latest_analysis),
        recent_comments=[CommentResponse.model_validate(c) for c in recent_comments],
        topics=[TopicResponse.model_validate(t) for t in topics],
        sentiment_distribution=sentiment_dist,
        sentiment_timeline=[],  # Can be enhanced with time-series data
        risk_level=risk_level
    )
