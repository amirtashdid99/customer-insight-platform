from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application configuration settings"""
    
    # App Settings
    APP_NAME: str = "Customer Insight Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    
    # Redis (for background tasks)
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Demo Mode (use mock data instead of real scraping)
    DEMO_MODE: bool = False
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    
    # Email (for notifications)
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str = ""  # Optional: Set for email alerts
    EMAIL_PASSWORD: str = ""  # Optional: App password for Gmail
    
    # Frontend URL (for email links)
    FRONTEND_URL: str = "http://localhost:3000"
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # ML Models
    SENTIMENT_MODEL_PATH: str = "../trained_models/sentiment_model"
    CHURN_MODEL_PATH: str = "../trained_models/churn_model.pkl"
    
    # Scraping
    MAX_SCRAPE_RESULTS: int = 50
    SCRAPE_TIMEOUT: int = 30
    USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
