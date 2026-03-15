from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from ..schemas.pydantic_models import DriftReport
from ..database.db import get_db
from ..monitoring.drift_detection import generate_drift_report
from ..database.models import DriftAlert, ModelRun

router = APIRouter()

@router.get("/drift/status", response_model=List[DriftReport])
async def get_drift_status(db: Session = Depends(get_db)):
    """Get current drift status for all features"""
    features = ['rsi', 'macd', 'close', 'volume', 'atr']
    reports = []
    
    for feature in features:
        report = generate_drift_report(db, feature)
        reports.append(DriftReport(**report))
    
    return reports

@router.get("/drift/alerts")
async def get_drift_alerts(db: Session = Depends(get_db)):
    """Get recent drift alerts"""
    alerts = db.query(DriftAlert).order_by(DriftAlert.created_at.desc()).limit(50).all()
    return [
        {
            "feature_name": a.feature_name,
            "psi_value": a.psi_value,
            "ks_statistic": a.ks_statistic,
            "alert_level": a.alert_level,
            "created_at": a.created_at
        } for a in alerts
    ]

@router.get("/system/status")
async def system_status(db: Session = Depends(get_db)):
    """Comprehensive system health and status"""
    model_runs = db.query(ModelRun).filter(ModelRun.is_active == True).all()
    latest_data = db.query(DataPoint).order_by(DataPoint.timestamp.desc()).first()
    
    return {
        "models": {
            "active_models": len(model_runs),
            "models": [
                {
                    "name": m.model_name,
                    "rmse": m.rmse,
                    "mae": m.mae,
                    "accuracy": m.directional_accuracy
                } for m in model_runs
            ]
        },
        "data": {
            "latest_timestamp": latest_data.timestamp.isoformat() if latest_data else None,
            "total_records": db.query(DataPoint).count()
        }
    }

@router.post("/drift/check")
async def manual_drift_check(feature: str, db: Session = Depends(get_db)):
    """Manual drift check for specific feature"""
    report = generate_drift_report(db, feature)
    return DriftReport(**report)

