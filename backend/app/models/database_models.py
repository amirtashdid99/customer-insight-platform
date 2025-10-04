from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class SentimentType(str, enum.Enum):
    """Enum for sentiment classification"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class AnalysisStatus(str, enum.Enum):
    """Enum for analysis job status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Product(Base):
    """Product/Company being tracked"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    analyses = relationship("Analysis", back_populates="product", cascade="all, delete-orphan")
    comments = relationship("CustomerComment", back_populates="product", cascade="all, delete-orphan")


class Analysis(Base):
    """Analysis job for a product"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, nullable=False)
    
    # Aggregated metrics
    total_comments = Column(Integer, default=0)
    avg_sentiment_score = Column(Float, nullable=True)  # -1 to 1
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    churn_risk_score = Column(Float, nullable=True)  # 0 to 1
    
    # Metadata
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    product = relationship("Product", back_populates="analyses")
    comments = relationship("CustomerComment", back_populates="analysis", cascade="all, delete-orphan")
    topics = relationship("Topic", back_populates="analysis", cascade="all, delete-orphan")


class CustomerComment(Base):
    """Individual customer comment/review"""
    __tablename__ = "customer_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    
    # Comment data
    text = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)  # e.g., "reddit", "twitter", "review_site"
    source_url = Column(String(500), nullable=True)
    author = Column(String(255), nullable=True)
    
    # Sentiment analysis results
    sentiment = Column(Enum(SentimentType), nullable=True)
    sentiment_score = Column(Float, nullable=True)  # -1 to 1
    confidence = Column(Float, nullable=True)  # 0 to 1
    
    # Timestamps
    posted_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="comments")
    analysis = relationship("Analysis", back_populates="comments")


class Topic(Base):
    """Topics extracted from customer comments"""
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=False)
    
    name = Column(String(100), nullable=False)
    keywords = Column(Text, nullable=True)  # Comma-separated keywords
    mention_count = Column(Integer, default=0)
    avg_sentiment = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    analysis = relationship("Analysis", back_populates="topics")


class User(Base):
    """User accounts for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    notification_preferences = relationship("NotificationPreference", back_populates="user", cascade="all, delete-orphan")
    saved_products = relationship("SavedProduct", back_populates="user", cascade="all, delete-orphan")


class NotificationPreference(Base):
    """User notification settings for products"""
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    email_alerts = Column(Boolean, default=True)
    sentiment_threshold = Column(Float, default=0.2)  # Alert if change > 20%
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notification_preferences")
    product = relationship("Product")


class SavedProduct(Base):
    """Products saved/tracked by users"""
    __tablename__ = "saved_products"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    nickname = Column(String(255), nullable=True)  # Optional custom name
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="saved_products")
    product = relationship("Product")
