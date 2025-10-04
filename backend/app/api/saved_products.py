"""
Saved Products API
Allow users to track and manage their favorite products
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
import logging

from app.core.database import get_db
from app.models.database_models import User, Product, SavedProduct, Analysis
from app.models.schemas import SavedProductCreate, SavedProductResponse
from app.api.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/saved-products", tags=["saved_products"])


@router.post("/", response_model=SavedProductResponse)
def save_product(
    data: SavedProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a product to user's tracked list
    
    Allows users to:
    - Track products they care about
    - Add custom nicknames
    - Add personal notes
    """
    # Get or create product
    product = db.query(Product).filter(Product.name == data.product_name).first()
    if not product:
        product = Product(name=data.product_name)
        db.add(product)
        db.commit()
        db.refresh(product)
    
    # Check if already saved
    existing = db.query(SavedProduct).filter(
        SavedProduct.user_id == current_user.id,
        SavedProduct.product_id == product.id
    ).first()
    
    if existing:
        # Update existing
        existing.nickname = data.nickname
        existing.notes = data.notes
        db.commit()
        db.refresh(existing)
        saved_product = existing
    else:
        # Create new
        saved_product = SavedProduct(
            user_id=current_user.id,
            product_id=product.id,
            nickname=data.nickname,
            notes=data.notes
        )
        db.add(saved_product)
        db.commit()
        db.refresh(saved_product)
    
    # Get latest analysis info
    latest_analysis = db.query(Analysis).filter(
        Analysis.product_id == product.id,
        Analysis.status == "completed"
    ).order_by(desc(Analysis.completed_at)).first()
    
    logger.info(f"User {current_user.email} saved product: {product.name}")
    
    return {
        "id": saved_product.id,
        "product_name": product.name,
        "nickname": saved_product.nickname,
        "notes": saved_product.notes,
        "created_at": saved_product.created_at,
        "last_analysis": latest_analysis.completed_at if latest_analysis else None,
        "latest_sentiment": _get_sentiment_label(latest_analysis) if latest_analysis else None
    }


@router.get("/", response_model=List[SavedProductResponse])
def get_saved_products(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all products saved by the current user
    
    Returns list with latest analysis info
    """
    saved_products = db.query(SavedProduct).filter(
        SavedProduct.user_id == current_user.id
    ).order_by(desc(SavedProduct.created_at)).all()
    
    result = []
    for sp in saved_products:
        product = db.query(Product).filter(Product.id == sp.product_id).first()
        
        # Get latest analysis
        latest_analysis = db.query(Analysis).filter(
            Analysis.product_id == product.id,
            Analysis.status == "completed"
        ).order_by(desc(Analysis.completed_at)).first()
        
        result.append({
            "id": sp.id,
            "product_name": product.name,
            "nickname": sp.nickname,
            "notes": sp.notes,
            "created_at": sp.created_at,
            "last_analysis": latest_analysis.completed_at if latest_analysis else None,
            "latest_sentiment": _get_sentiment_label(latest_analysis) if latest_analysis else None
        })
    
    return result


@router.delete("/{saved_product_id}")
def remove_saved_product(
    saved_product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a product from saved list
    """
    saved_product = db.query(SavedProduct).filter(
        SavedProduct.id == saved_product_id,
        SavedProduct.user_id == current_user.id
    ).first()
    
    if not saved_product:
        raise HTTPException(status_code=404, detail="Saved product not found")
    
    product = db.query(Product).filter(Product.id == saved_product.product_id).first()
    logger.info(f"User {current_user.email} removed saved product: {product.name}")
    
    db.delete(saved_product)
    db.commit()
    
    return {"message": f"Removed {product.name} from saved products"}


def _get_sentiment_label(analysis: Analysis) -> str:
    """Helper to get sentiment label from analysis"""
    if not analysis or analysis.total_comments == 0:
        return "unknown"
    
    pos_ratio = analysis.positive_count / analysis.total_comments
    neg_ratio = analysis.negative_count / analysis.total_comments
    
    if pos_ratio > 0.6:
        return "positive"
    elif neg_ratio > 0.4:
        return "negative"
    else:
        return "mixed"
