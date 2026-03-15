from celery import shared_task
from .binance_collector import collector
from database.db import SessionLocal
import logging

logger = logging.getLogger(__name__)

@shared_task
def ingest_data():
    """Celery task to ingest new BTC data"""
    db = SessionLocal()
    try:
        df = collector.fetch_ohlcv()
        collector.save_to_db(df, db)
        logger.info("Data ingestion task completed successfully")
    except Exception as e:
        logger.error(f"Data ingestion failed: {str(e)}")
        raise
    finally:
        db.close()

# Manual trigger function for testing
def run_ingestion():
    ingest_data.delay()

