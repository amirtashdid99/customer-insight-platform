"""
Web Scraping Service

This module scrapes customer reviews and comments from various sources.
Implements a unique multi-source scraping approach.
"""

import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import logging
import re
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


class Comment:
    """Data class for scraped comments"""
    
    def __init__(
        self,
        text: str,
        source: str,
        author: str = None,
        source_url: str = None,
        posted_at: datetime = None
    ):
        self.text = text
        self.source = source
        self.author = author
        self.source_url = source_url
        self.posted_at = posted_at or datetime.utcnow()


class WebScraper:
    """Multi-source web scraper for customer feedback"""
    
    def __init__(self, user_agent: str, timeout: int = 30):
        self.user_agent = user_agent
        self.timeout = timeout
        self.headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def scrape_reddit_style(self, product_name: str, max_results: int = 20) -> List[Comment]:
        """
        Simulate scraping Reddit-style discussions
        
        Note: In production, you'd use Reddit API or actual scraping.
        For demo purposes, this generates realistic synthetic data.
        """
        logger.info(f"Scraping Reddit-style comments for: {product_name}")
        
        comments = []
        
        # Realistic comment templates
        positive_templates = [
            f"I've been using {product_name} for months and it's amazing!",
            f"Best decision ever switching to {product_name}. Highly recommend!",
            f"{product_name} has exceeded my expectations. Great product!",
            f"Love {product_name}! Customer service is also fantastic.",
            f"Can't imagine going back after trying {product_name}.",
        ]
        
        negative_templates = [
            f"Really disappointed with {product_name}. Not worth the money.",
            f"{product_name} has too many bugs. Switching to a competitor.",
            f"Customer support for {product_name} is terrible. Never again.",
            f"Expected more from {product_name}. Quality has gone downhill.",
            f"Overpriced and underdelivering. {product_name} needs to improve.",
        ]
        
        neutral_templates = [
            f"{product_name} is okay, nothing special but gets the job done.",
            f"Mixed feelings about {product_name}. Some good, some bad.",
            f"It's average. {product_name} works but has room for improvement.",
            f"Not sure if I'll continue with {product_name}. Still deciding.",
            f"{product_name} meets basic needs but lacks innovation.",
        ]
        
        # Mix of sentiments (60% positive, 25% negative, 15% neutral)
        import random
        
        for i in range(min(max_results, 20)):
            rand = random.random()
            
            if rand < 0.60:
                text = random.choice(positive_templates)
                source_type = "reddit_positive"
            elif rand < 0.85:
                text = random.choice(negative_templates)
                source_type = "reddit_negative"
            else:
                text = random.choice(neutral_templates)
                source_type = "reddit_neutral"
            
            comment = Comment(
                text=text,
                source="reddit",
                author=f"user_{random.randint(1000, 9999)}",
                source_url=f"https://reddit.com/r/reviews/comments/{random.randint(100000, 999999)}",
                posted_at=datetime.utcnow()
            )
            comments.append(comment)
        
        logger.info(f"Scraped {len(comments)} Reddit-style comments")
        return comments
    
    async def scrape_review_sites(self, product_name: str, max_results: int = 15) -> List[Comment]:
        """
        Simulate scraping from review aggregator sites
        
        In production, you'd scrape sites like Trustpilot, G2, or Capterra
        """
        logger.info(f"Scraping review sites for: {product_name}")
        
        comments = []
        
        review_templates = [
            f"{product_name} transformed our workflow. 5 stars!",
            f"Good product but {product_name} needs better documentation.",
            f"Pricing of {product_name} is too high for what it offers.",
            f"Excellent features! {product_name} is our go-to solution.",
            f"Integration issues with {product_name}. Support was helpful though.",
            f"User interface of {product_name} could be more intuitive.",
            f"Reliable and stable. {product_name} just works.",
            f"Lots of features in {product_name} but steep learning curve.",
        ]
        
        import random
        
        for i in range(min(max_results, 15)):
            comment = Comment(
                text=random.choice(review_templates),
                source="trustpilot",
                author=f"reviewer_{random.randint(100, 999)}",
                source_url=f"https://trustpilot.com/review/{product_name.lower().replace(' ', '-')}",
                posted_at=datetime.utcnow()
            )
            comments.append(comment)
        
        logger.info(f"Scraped {len(comments)} review site comments")
        return comments
    
    async def scrape_twitter_style(self, product_name: str, max_results: int = 15) -> List[Comment]:
        """
        Simulate Twitter/X sentiment scraping
        
        In production, use Twitter API v2
        """
        logger.info(f"Scraping Twitter-style posts for: {product_name}")
        
        comments = []
        
        tweet_templates = [
            f"Just tried {product_name} and I'm impressed! 🚀",
            f"Why is {product_name} so expensive? Not happy 😒",
            f"@{product_name.replace(' ', '')} your product rocks! 💪",
            f"Thinking of canceling my {product_name} subscription...",
            f"{product_name} update is fire! Great improvements 🔥",
            f"Had issues with {product_name} today. Frustrating experience.",
            f"Shoutout to {product_name} team for excellent support! 👏",
            f"{product_name} vs competitors? Not seeing the value tbh",
        ]
        
        import random
        
        for i in range(min(max_results, 15)):
            comment = Comment(
                text=random.choice(tweet_templates),
                source="twitter",
                author=f"@user{random.randint(100, 999)}",
                source_url=f"https://twitter.com/status/{random.randint(1000000, 9999999)}",
                posted_at=datetime.utcnow()
            )
            comments.append(comment)
        
        logger.info(f"Scraped {len(comments)} Twitter-style comments")
        return comments
    
    async def scrape_all_sources(self, product_name: str, max_results: int = 50) -> List[Comment]:
        """
        Scrape from all available sources concurrently
        
        Args:
            product_name: Name of product/company to search for
            max_results: Maximum total results to return
            
        Returns:
            List of Comment objects
        """
        logger.info(f"Starting multi-source scraping for: {product_name}")
        
        # Distribute max_results across sources
        reddit_limit = int(max_results * 0.4)
        review_limit = int(max_results * 0.3)
        twitter_limit = int(max_results * 0.3)
        
        # Run scrapers concurrently
        tasks = [
            self.scrape_reddit_style(product_name, reddit_limit),
            self.scrape_review_sites(product_name, review_limit),
            self.scrape_twitter_style(product_name, twitter_limit)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine all comments
        all_comments = []
        for result in results:
            if isinstance(result, list):
                all_comments.extend(result)
            else:
                logger.error(f"Scraper error: {result}")
        
        logger.info(f"Total comments scraped: {len(all_comments)}")
        return all_comments[:max_results]


def create_scraper(user_agent: str, timeout: int = 30) -> WebScraper:
    """Factory function to create a web scraper instance"""
    return WebScraper(user_agent, timeout)
