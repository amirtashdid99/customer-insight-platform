"""
Analysis API Endpoints

This module contains the core API endpoints for analyzing products.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
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
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/analyze", response_model=AnalysisJobResponse)
async def start_analysis(
    request: AnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Start a new analysis job for a product
    
    This endpoint:
    1. Creates or finds the product in the database
    2. Creates a new analysis record
    3. In DEMO mode: Runs synchronously with mock data (no Celery/Redis needed)
    4. In FULL mode: Queues background task to Celery worker
    5. Returns immediately with job ID
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
        
        # Choose execution mode based on DEMO_MODE setting
        if settings.DEMO_MODE:
            # DEMO MODE: Run synchronously without Celery/Redis
            logger.info(f"Running analysis {analysis.id} in DEMO mode (no Celery)")
            from app.tasks.analysis_tasks import run_analysis_sync
            # Run in background to avoid blocking the API response
            import asyncio
            asyncio.create_task(
                asyncio.to_thread(run_analysis_sync, analysis.id, request.product_name)
            )
            estimated_time = 5  # Demo mode is faster
        else:
            # FULL MODE: Queue to Celery worker (requires Redis)
            from app.tasks.analysis_tasks import run_analysis_task
            task = run_analysis_task.delay(analysis.id, request.product_name)
            logger.info(f"Queued analysis task {task.id} for analysis {analysis.id}")
            estimated_time = 90  # Real scraping takes longer
        
        return AnalysisJobResponse(
            message=f"Analysis started for '{request.product_name}'",
            analysis_id=analysis.id,
            status=analysis.status,
            estimated_time_seconds=estimated_time
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
