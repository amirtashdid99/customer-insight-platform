"""
Churn Prediction Service

This module loads the trained XGBoost model and provides churn prediction
functionality based on aggregated customer sentiment data.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ChurnPredictor:
    """Churn prediction using trained XGBoost model"""
    
    def __init__(self, model_path: str):
        """
        Initialize churn predictor
        
        Args:
            model_path: Path to the directory containing the trained model
        """
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = None
        self.feature_names = None
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and preprocessing objects"""
        try:
            logger.info(f"Loading churn model from {self.model_path}")
            
            # Load model
            model_file = self.model_path / "churn_model.pkl"
            if model_file.exists():
                self.model = joblib.load(model_file)
                
                # Load scaler
                scaler_file = self.model_path / "scaler.pkl"
                self.scaler = joblib.load(scaler_file)
                
                logger.info("Churn model loaded successfully")
            else:
                logger.warning(f"Model file not found at {model_file}. Using sentiment-based algorithm.")
                self.model = None
                self.scaler = None
            
        except Exception as e:
            logger.warning(f"Failed to load churn model: {e}. Using sentiment-based algorithm.")
            self.model = None
            self.scaler = None
    
    def predict_churn_from_sentiment(
        self, 
        avg_sentiment: float,
        negative_ratio: float,
        total_comments: int,
        sentiment_volatility: float = 0.0
    ) -> Dict[str, any]:
        """
        Predict churn risk based on sentiment analysis results
        
        This is a custom approach that maps sentiment metrics to churn probability.
        Since we're analyzing products/companies (not individual customers), we
        create synthetic features based on sentiment that correlate with churn.
        
        Args:
            avg_sentiment: Average sentiment score (-1 to 1)
            negative_ratio: Ratio of negative comments (0 to 1)
            total_comments: Total number of comments analyzed
            sentiment_volatility: Volatility/variance in sentiment scores
            
        Returns:
            Dictionary with churn probability and risk level
        """
        
        # Normalize inputs
        avg_sentiment = max(-1, min(1, avg_sentiment))  # Clamp to [-1, 1]
        negative_ratio = max(0, min(1, negative_ratio))  # Clamp to [0, 1]
        
        # Calculate churn risk using a weighted formula
        # Higher negative sentiment and volatility = higher churn risk
        
        # Base risk from sentiment
        sentiment_risk = (1 - avg_sentiment) / 2  # Convert -1 to 1 => 1 to 0
        
        # Boost risk if many negative comments
        negative_boost = negative_ratio * 0.3
        
        # Volatility adds uncertainty (small boost)
        volatility_boost = min(sentiment_volatility, 0.2)
        
        # Comment volume factor (very few comments = less reliable)
        volume_factor = min(total_comments / 50, 1.0)  # Full confidence at 50+ comments
        
        # Combine factors
        churn_probability = (
            sentiment_risk * 0.5 +
            negative_boost +
            volatility_boost
        ) * volume_factor
        
        # Clamp to [0, 1]
        churn_probability = max(0, min(1, churn_probability))
        
        # Determine risk level
        if churn_probability < 0.3:
            risk_level = "low"
        elif churn_probability < 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        return {
            "churn_probability": round(churn_probability, 3),
            "risk_level": risk_level,
            "confidence": round(volume_factor, 3)
        }
    
    def predict_from_features(self, features: np.ndarray) -> float:
        """
        Predict churn using actual model features (if available)
        
        This method would be used if you have real customer data
        matching the Telco dataset structure.
        
        Args:
            features: Feature array matching training data format
            
        Returns:
            Churn probability (0 to 1)
        """
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            # Scale features
            features_scaled = self.scaler.transform(features.reshape(1, -1))
            
            # Predict probability
            probability = self.model.predict_proba(features_scaled)[0, 1]
            
            return float(probability)
            
        except Exception as e:
            logger.error(f"Error predicting churn: {e}")
            return 0.5  # Return neutral probability on error


# Global instance (lazy loading)
_churn_predictor = None


def get_churn_predictor(model_path: str = "../trained_models") -> ChurnPredictor:
    """Get or create the global churn predictor instance"""
    global _churn_predictor
    if _churn_predictor is None:
        _churn_predictor = ChurnPredictor(model_path)
    return _churn_predictor
