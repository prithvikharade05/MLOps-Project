from celery import chain, group
from ingestion.scheduler import ingest_data
from features.feature_pipeline import run_feature_pipeline
from models.train_linear_regression import train_linear_model
from models.train_arima import train_arima_model
from monitoring.drift_detection import generate_drift_report
from database.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

@celery.task
def create_features():
    """Feature engineering task"""
    db = SessionLocal()
    try:
        run_feature_pipeline(db)
    finally:
        db.close()

@celery.task
def train_models():
    """Train all models"""
    chain(
        train_linear_model.s(),
        train_arima_model.s()
    ).apply_async()

@celery.task
def run_drift_check():
    """Run drift detection on all features"""
    db = SessionLocal()
    features = ['rsi', 'macd', 'close', 'volume']
    results = []
    try:
        for feature in features:
            result = generate_drift_report(db, feature)
            results.append(result)
    finally:
        db.close()
    return results

# Full pipeline workflows
full_pipeline = chain(
    ingest_data.s(),
    create_features.s(),
    train_models.s(),
    run_drift_check.s()
)

hourly_pipeline = chain(
    ingest_data.s(),
    create_features.s(),
    run_drift_check.s()
)

daily_pipeline = chain(
    ingest_data.s(),
    create_features.s(),
    train_models.s()
)

