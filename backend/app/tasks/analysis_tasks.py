"""
Celery background tasks for analysis processing
"""
from celery import Task
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.database_models import (
    Product, Analysis, CustomerComment, Topic,
    AnalysisStatus, SentimentType
)
from app.scrapers import create_scraper
from app.ml import get_sentiment_analyzer, get_churn_predictor
from app.core.config import settings
from datetime import datetime
from typing import List
import logging

logger = logging.getLogger(__name__)


class DatabaseTask(Task):
    """Base task with database session management"""
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = SessionLocal()
        return self._db

    def after_return(self, *args, **kwargs):
        if self._db is not None:
            self._db.close()
            self._db = None


def extract_topics(texts: List[str], sentiments: List[dict]) -> dict:
    """
    Simple topic extraction based on common keywords
    """
    from collections import defaultdict
    import re
    
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
            for kw in keywords:
                if kw in text_lower:
                    topics[topic]["count"] += 1
                    topics[topic]["sentiments"].append(sentiment['score'])
                    if kw not in ["$"]:
                        topics[topic]["keywords"].add(kw)
    
    # Calculate average sentiment for each topic
    result = {}
    for topic, data in topics.items():
        if data["count"] > 0:
            result[topic] = {
                "count": data["count"],
                "keywords": list(data["keywords"])[:5],
                "avg_sentiment": sum(data["sentiments"]) / len(data["sentiments"])
            }
    
    return result


@celery_app.task(bind=True, base=DatabaseTask, name='app.tasks.run_analysis')
def run_analysis_task(self, analysis_id: int, product_name: str):
    """
    Background task to run the complete analysis pipeline
    
    Steps:
    1. Scrape customer comments from web
    2. Run sentiment analysis on each comment
    3. Calculate aggregate metrics
    4. Predict churn risk
    5. Extract topics
    6. Update analysis status
    """
    db = self.db
    
    try:
        # Update status to in_progress
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return {"error": "Analysis not found"}
        
        analysis.status = AnalysisStatus.IN_PROGRESS
        db.commit()
        
        logger.info(f"Starting analysis task {analysis_id} for product: {product_name}")
        
        # Update task progress
        self.update_state(state='PROGRESS', meta={'step': 'scraping', 'progress': 10})
        
        # Step 1: Scrape or generate data based on DEMO_MODE
        if settings.DEMO_MODE:
            # Demo Mode: Use sample data (for online demo)
            from app.models.schemas import ScrapedComment
            from datetime import datetime, timedelta
            import random
            
            logger.info("DEMO MODE: Using sample data")
            
            # Realistic sample comments
            sample_templates = {
                'positive': [
                    f"Great {product_name}! Really impressed with the quality and features.",
                    f"Absolutely love my {product_name}! Best purchase ever.",
                    f"The {product_name} exceeded my expectations. Highly recommend!",
                    f"Five stars! {product_name} is exactly what I needed.",
                    f"Best {product_name} on the market. Worth every penny!",
                ],
                'negative': [
                    f"Not happy with {product_name}. Customer service was terrible.",
                    f"Disappointed with {product_name}. Expected better quality.",
                    f"The {product_name} broke after just one week. Avoid!",
                    f"Waste of money. {product_name} doesn't work as advertised.",
                    f"Poor quality {product_name}. Don't recommend at all.",
                ],
                'neutral': [
                    f"The {product_name} is okay but has some issues with battery life.",
                    f"Average product. Nothing special about {product_name}.",
                    f"{product_name} is decent for the price but could be better.",
                    f"Mixed feelings about {product_name}. Some pros and cons.",
                    f"It's alright. {product_name} does the job but nothing impressive.",
                ]
            }
            
            sources = ['Amazon', 'Reddit', 'Twitter', 'Trustpilot', 'Google Reviews']
            comments = []
            
            # Generate 15-25 random comments with mixed sentiment
            num_comments = random.randint(15, 25)
            
            for i in range(num_comments):
                rand = random.random()
                if rand < 0.50:  # 50% positive
                    sentiment_type = 'positive'
                elif rand < 0.80:  # 30% negative
                    sentiment_type = 'negative'
                else:  # 20% neutral
                    sentiment_type = 'neutral'
                
                comment = ScrapedComment(
                    text=random.choice(sample_templates[sentiment_type]),
                    source=random.choice(sources),
                    source_url=f"https://example.com/{product_name.lower().replace(' ', '-')}",
                    author=f"User{i+1}",
                    posted_at=datetime.now() - timedelta(days=random.randint(0, 30))
                )
                comments.append(comment)
            
            logger.info(f"Generated {len(comments)} sample comments for demo")
        else:
            # Production Mode: Real web scraping
            import asyncio
            
            logger.info("PRODUCTION MODE: Real web scraping")
            scraper = create_scraper(
                user_agent=settings.USER_AGENT,
                timeout=settings.SCRAPE_TIMEOUT
            )
            
            # Run async scraping in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                comments = loop.run_until_complete(
                    scraper.scrape_all_sources(
                        product_name,
                        max_results=settings.MAX_SCRAPE_RESULTS
                    )
                )
            finally:
                loop.close()
            
            if not comments:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = "No comments found"
                db.commit()
                return {"error": "No comments found"}
            
            logger.info(f"Scraped {len(comments)} real comments")
        self.update_state(state='PROGRESS', meta={'step': 'sentiment_analysis', 'progress': 40})
        
        # Step 2: Sentiment analysis
        sentiment_analyzer = get_sentiment_analyzer()
        texts = [c.text for c in comments]
        sentiments = sentiment_analyzer.analyze_batch(texts)
        
        self.update_state(state='PROGRESS', meta={'step': 'saving_data', 'progress': 60})
        
        # Step 3: Save comments to database
        comment_objects = []
        sentiment_scores = []
        
        for comment, sentiment in zip(comments, sentiments):
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
        
        self.update_state(state='PROGRESS', meta={'step': 'calculating_metrics', 'progress': 70})
        
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
        
        self.update_state(state='PROGRESS', meta={'step': 'extracting_topics', 'progress': 85})
        
        # Step 6: Extract topics
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
        
        # Step 7: Update analysis with final results
        analysis.status = AnalysisStatus.COMPLETED
        analysis.total_comments = total
        analysis.positive_count = positive
        analysis.negative_count = negative
        analysis.neutral_count = neutral
        analysis.avg_sentiment_score = avg_sentiment
        analysis.churn_risk_score = churn_result['churn_probability']
        analysis.completed_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Analysis task {analysis_id} completed successfully")
        
        return {
            "status": "completed",
            "analysis_id": analysis_id,
            "total_comments": total,
            "avg_sentiment": avg_sentiment
        }
        
    except Exception as e:
        logger.error(f"Error in analysis task {analysis_id}: {e}", exc_info=True)
        
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = str(e)
            db.commit()
        
        raise
