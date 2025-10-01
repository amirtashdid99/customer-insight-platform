from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.database_models import SentimentType, AnalysisStatus


# Product Schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Comment Schemas
class CommentBase(BaseModel):
    text: str
    source: str
    source_url: Optional[str] = None
    author: Optional[str] = None
    posted_at: Optional[datetime] = None


class ScrapedComment(BaseModel):
    """Schema for scraped comments (used in scraping and demo mode)"""
    text: str
    source: str
    source_url: str
    author: str
    posted_at: datetime


class CommentResponse(CommentBase):
    id: int
    sentiment: Optional[SentimentType] = None
    sentiment_score: Optional[float] = None
    confidence: Optional[float] = None
    scraped_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Topic Schemas
class TopicResponse(BaseModel):
    id: int
    name: str
    keywords: Optional[str] = None
    mention_count: int
    avg_sentiment: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)


# Analysis Schemas
class AnalysisRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=255)


class AnalysisResponse(BaseModel):
    id: int
    product_id: int
    status: AnalysisStatus
    total_comments: int
    avg_sentiment_score: Optional[float] = None
    positive_count: int
    negative_count: int
    neutral_count: int
    churn_risk_score: Optional[float] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class DashboardData(BaseModel):
    """Comprehensive dashboard data response"""
    product: ProductResponse
    latest_analysis: Optional[AnalysisResponse] = None
    recent_comments: List[CommentResponse] = []
    topics: List[TopicResponse] = []
    
    # Additional computed metrics
    sentiment_distribution: dict = Field(
        default_factory=dict,
        description="Distribution of sentiments {positive: %, negative: %, neutral: %}"
    )
    sentiment_timeline: List[dict] = Field(
        default_factory=list,
        description="Time-series data for sentiment trends"
    )
    risk_level: Optional[str] = Field(
        None,
        description="Human-readable risk level: low, medium, high"
    )


class AnalysisJobResponse(BaseModel):
    """Response after initiating an analysis"""
    message: str
    analysis_id: int
    status: AnalysisStatus
    estimated_time_seconds: int = Field(
        default=60,
        description="Estimated time to complete analysis"
    )
