from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database.db import get_db
from ..database.models import DataPoint, ModelRun
from typing import Dict, Any, List
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/performance")
async def get_model_performance(db: Session = Depends(get_db)):
    """Get model performance metrics"""
    models = db.query(ModelRun).filter(ModelRun.is_active == True).all()
    
    return {
        "models": [
            {
                "name": m.model_name,
                "version": m.version,
                "rmse": float(m.rmse),
                "mae": float(m.mae),
                "directional_accuracy": float(m.directional_accuracy),
                "created_at": m.created_at.isoformat()
            } for m in models
        ]
    }

@router.get("/data/stats")
async def get_data_stats(db: Session = Depends(get_db)):
    """Get data statistics"""
    total_records = db.query(DataPoint).count()
    latest = db.query(DataPoint).order_by(DataPoint.timestamp.desc()).first()
    oldest = db.query(DataPoint).order_by(DataPoint.timestamp.asc()).first()
    
    if latest and oldest:
        data_span = latest.timestamp - oldest.timestamp
    else:
        data_span = None
    
    recent_24h = db.query(DataPoint).filter(
        DataPoint.timestamp > datetime.utcnow() - timedelta(hours=24)
    ).count()
    
    return {
        "total_records": total_records,
        "recent_24h": recent_24h,
        "data_span_hours": data_span.total_seconds() / 3600 if data_span else 0,
        "latest_timestamp": latest.timestamp.isoformat() if latest else None
    }

@router.get("/features/distribution")
async def get_feature_distribution(db: Session = Depends(get_db)):
    """Get feature distribution stats"""
    features = ['rsi', 'macd', 'atr']
    stats = {}
    
    for feature in features:
        values = db.query(getattr(DataPoint, feature)).all()
        values = [v for v in values if v is not None]
        
        if values:
            stats[feature] = {
                "count": len(values),
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values))
            }
    
    return stats

