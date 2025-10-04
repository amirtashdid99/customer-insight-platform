"""
Email Notification System
Send alerts when sentiment spikes are detected
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from app.core.database import get_db
from app.core.config import settings
from app.models.database_models import User, Product, Analysis, NotificationPreference, SentimentType
from app.models.schemas import NotificationPreferenceCreate, NotificationResponse
from app.api.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/notifications", tags=["notifications"])


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send email notification
    
    Configure SMTP settings in .env:
    - EMAIL_HOST
    - EMAIL_PORT
    - EMAIL_USERNAME
    - EMAIL_PASSWORD
    """
    try:
        if not all([settings.EMAIL_HOST, settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD]):
            logger.warning("Email not configured. Skipping email notification.")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.EMAIL_USERNAME
        msg['To'] = to_email
        
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False


def check_sentiment_spike(product_id: int, db: Session) -> dict:
    """
    Check if there's a significant sentiment spike
    
    Returns alert info if spike detected, None otherwise
    """
    # Get last 2 analyses
    analyses = db.query(Analysis).filter(
        Analysis.product_id == product_id,
        Analysis.status == "completed"
    ).order_by(desc(Analysis.completed_at)).limit(2).all()
    
    if len(analyses) < 2:
        return None
    
    current = analyses[0]
    previous = analyses[1]
    
    # Calculate sentiment change
    current_negative_ratio = current.negative_count / max(current.total_comments, 1)
    previous_negative_ratio = previous.negative_count / max(previous.total_comments, 1)
    
    change = current_negative_ratio - previous_negative_ratio
    
    # Alert if negative sentiment increased by >20%
    if change > 0.20:
        return {
            "type": "negative_spike",
            "change_percentage": round(change * 100, 1),
            "current_negative_ratio": round(current_negative_ratio * 100, 1),
            "previous_negative_ratio": round(previous_negative_ratio * 100, 1),
            "analysis_id": current.id
        }
    
    # Alert if positive sentiment increased by >30%
    current_positive_ratio = current.positive_count / max(current.total_comments, 1)
    previous_positive_ratio = previous.positive_count / max(previous.total_comments, 1)
    positive_change = current_positive_ratio - previous_positive_ratio
    
    if positive_change > 0.30:
        return {
            "type": "positive_spike",
            "change_percentage": round(positive_change * 100, 1),
            "current_positive_ratio": round(current_positive_ratio * 100, 1),
            "previous_positive_ratio": round(previous_positive_ratio * 100, 1),
            "analysis_id": current.id
        }
    
    return None


def send_sentiment_alert(user: User, product: Product, spike_info: dict, db: Session):
    """Send sentiment spike alert email to user"""
    
    if spike_info["type"] == "negative_spike":
        subject = f"⚠️ Alert: Negative Sentiment Spike for {product.name}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #dc2626;">⚠️ Negative Sentiment Alert</h2>
            <p>Hello {user.full_name},</p>
            <p>We detected a significant increase in negative sentiment for <strong>{product.name}</strong>:</p>
            <ul>
                <li><strong>Negative sentiment increased by {spike_info['change_percentage']}%</strong></li>
                <li>Current: {spike_info['current_negative_ratio']}% negative</li>
                <li>Previous: {spike_info['previous_negative_ratio']}% negative</li>
            </ul>
            <p>⚠️ <strong>Recommendation:</strong> Review recent customer feedback immediately and address concerns.</p>
            <p style="margin-top: 30px;">
                <a href="{settings.FRONTEND_URL}/dashboard/{product.name}" 
                   style="background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                    View Dashboard
                </a>
            </p>
            <p style="color: #6b7280; font-size: 0.9rem; margin-top: 30px;">
                Customer Insight Platform - Real-time Sentiment Monitoring
            </p>
        </body>
        </html>
        """
    else:  # positive_spike
        subject = f"🎉 Great News: Positive Sentiment Surge for {product.name}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #10b981;">🎉 Positive Sentiment Alert</h2>
            <p>Hello {user.full_name},</p>
            <p>Great news! There's a significant increase in positive sentiment for <strong>{product.name}</strong>:</p>
            <ul>
                <li><strong>Positive sentiment increased by {spike_info['change_percentage']}%</strong></li>
                <li>Current: {spike_info['current_positive_ratio']}% positive</li>
                <li>Previous: {spike_info['previous_positive_ratio']}% positive</li>
            </ul>
            <p>✅ <strong>Recommendation:</strong> Leverage this positive momentum in your marketing!</p>
            <p style="margin-top: 30px;">
                <a href="{settings.FRONTEND_URL}/dashboard/{product.name}" 
                   style="background: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                    View Dashboard
                </a>
            </p>
            <p style="color: #6b7280; font-size: 0.9rem; margin-top: 30px;">
                Customer Insight Platform - Real-time Sentiment Monitoring
            </p>
        </body>
        </html>
        """
    
    send_email(user.email, subject, body)


@router.post("/preferences", response_model=NotificationResponse)
def set_notification_preferences(
    prefs: NotificationPreferenceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Set notification preferences for a product
    
    User can enable email alerts for sentiment spikes
    """
    # Check if product exists
    product = db.query(Product).filter(Product.name == prefs.product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if preference already exists
    existing_pref = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id,
        NotificationPreference.product_id == product.id
    ).first()
    
    if existing_pref:
        existing_pref.email_alerts = prefs.email_alerts
        existing_pref.sentiment_threshold = prefs.sentiment_threshold
        db.commit()
        db.refresh(existing_pref)
        return {
            "message": "Notification preferences updated",
            "product_name": product.name,
            "email_alerts": existing_pref.email_alerts
        }
    else:
        new_pref = NotificationPreference(
            user_id=current_user.id,
            product_id=product.id,
            email_alerts=prefs.email_alerts,
            sentiment_threshold=prefs.sentiment_threshold
        )
        db.add(new_pref)
        db.commit()
        db.refresh(new_pref)
        return {
            "message": "Notification preferences created",
            "product_name": product.name,
            "email_alerts": new_pref.email_alerts
        }


@router.get("/preferences/{product_name}")
def get_notification_preferences(
    product_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification preferences for a product"""
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    pref = db.query(NotificationPreference).filter(
        NotificationPreference.user_id == current_user.id,
        NotificationPreference.product_id == product.id
    ).first()
    
    if not pref:
        return {
            "product_name": product_name,
            "email_alerts": False,
            "sentiment_threshold": 0.2
        }
    
    return {
        "product_name": product_name,
        "email_alerts": pref.email_alerts,
        "sentiment_threshold": pref.sentiment_threshold
    }


@router.post("/check-alerts/{analysis_id}")
def check_and_send_alerts(
    analysis_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Check for sentiment spikes and send alerts
    
    Called automatically after analysis completes
    """
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    product = db.query(Product).filter(Product.id == analysis.product_id).first()
    
    # Check for sentiment spike
    spike_info = check_sentiment_spike(product.id, db)
    
    if not spike_info:
        return {"message": "No significant sentiment changes detected"}
    
    # Get users with notifications enabled for this product
    preferences = db.query(NotificationPreference).filter(
        NotificationPreference.product_id == product.id,
        NotificationPreference.email_alerts == True
    ).all()
    
    if not preferences:
        return {"message": f"Spike detected but no users are subscribed", "spike_info": spike_info}
    
    # Send alerts to subscribed users
    for pref in preferences:
        user = db.query(User).filter(User.id == pref.user_id).first()
        if user:
            background_tasks.add_task(send_sentiment_alert, user, product, spike_info, db)
    
    logger.info(f"Sentiment spike detected for {product.name}, alerts sent to {len(preferences)} users")
    
    return {
        "message": f"Alerts sent to {len(preferences)} users",
        "spike_info": spike_info
    }
