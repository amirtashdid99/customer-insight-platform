"""
Sentiment Analysis Service using Hugging Face Transformers

This module provides sentiment analysis capabilities using a pre-trained
or fine-tuned transformer model.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class SentimentAnalyzer:
    """Sentiment analysis using transformer models"""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        """
        Initialize sentiment analyzer
        
        Args:
            model_name: Hugging Face model name or path to local model
        """
        self.model_name = model_name
        self.device = 0 if torch.cuda.is_available() else -1
        
        logger.info(f"Loading sentiment model: {model_name}")
        logger.info(f"Using device: {'GPU' if self.device == 0 else 'CPU'}")
        
        try:
            # Load pipeline for sentiment analysis
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=model_name,
                device=self.device,
                truncation=True,
                max_length=512
            )
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentiment model: {e}")
            raise
    
    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of a single text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment, score, and confidence
        """
        if not text or not text.strip():
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.0
            }
        
        try:
            # Run inference
            result = self.pipeline(text[:512])[0]  # Truncate long texts
            
            # Map label to our sentiment types
            label = result['label'].lower()
            confidence = result['score']
            
            # Convert to our format
            if label == 'positive' or label == 'pos':
                sentiment = "positive"
                score = confidence
            elif label == 'negative' or label == 'neg':
                sentiment = "negative"
                score = -confidence
            else:
                sentiment = "neutral"
                score = 0.0
            
            return {
                "sentiment": sentiment,
                "score": score,  # -1 to 1
                "confidence": confidence  # 0 to 1
            }
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                "sentiment": "neutral",
                "score": 0.0,
                "confidence": 0.0
            }
    
    def analyze_batch(self, texts: list) -> list:
        """
        Analyze sentiment for multiple texts (more efficient)
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of sentiment dictionaries
        """
        if not texts:
            return []
        
        try:
            # Truncate texts
            truncated_texts = [text[:512] if text else "" for text in texts]
            
            # Batch inference
            results = self.pipeline(truncated_texts)
            
            # Convert to our format
            analyzed = []
            for result in results:
                label = result['label'].lower()
                confidence = result['score']
                
                if label == 'positive' or label == 'pos':
                    sentiment = "positive"
                    score = confidence
                elif label == 'negative' or label == 'neg':
                    sentiment = "negative"
                    score = -confidence
                else:
                    sentiment = "neutral"
                    score = 0.0
                
                analyzed.append({
                    "sentiment": sentiment,
                    "score": score,
                    "confidence": confidence
                })
            
            return analyzed
            
        except Exception as e:
            logger.error(f"Error in batch sentiment analysis: {e}")
            # Return neutral results for all texts
            return [{"sentiment": "neutral", "score": 0.0, "confidence": 0.0} 
                    for _ in texts]


# Global instance (lazy loading)
_sentiment_analyzer = None


def get_sentiment_analyzer() -> SentimentAnalyzer:
    """Get or create the global sentiment analyzer instance"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer
