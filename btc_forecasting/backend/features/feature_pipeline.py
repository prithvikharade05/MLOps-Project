import pandas as pd
from sqlalchemy.orm import Session
from database.models import DataPoint
from .technical_indicators import (
    calculate_technical_indicators, 
    calculate_lag_features, 
    calculate_rolling_features, 
    calculate_target
)
import logging

logger = logging.getLogger(__name__)

def run_feature_pipeline(db: Session):
    """Full feature engineering pipeline"""
    # Fetch raw data
    data_points = db.query(DataPoint).order_by(DataPoint.timestamp).all()
    
    if not data_points:
        logger.warning("No raw data found for feature engineering")
        return
    
    df = pd.DataFrame([
        {
            'timestamp': dp.timestamp,
            'open': dp.open,
            'high': dp.high,
            'low': dp.low,
            'close': dp.close,
            'volume': dp.volume
        } for dp in data_points
    ])
    
    # Calculate features
    logger.info("Calculating technical indicators...")
    df = calculate_technical_indicators(df)
    
    logger.info("Calculating lag features...")
    df = calculate_lag_features(df)
    
    logger.info("Calculating rolling features...")
    df = calculate_rolling_features(df)
    
    logger.info("Calculating target...")
    df = calculate_target(df)
    
    # Update database with features
    for idx, row in df.iterrows():
        dp = data_points[idx]
        dp.rsi = row['rsi']
        dp.macd = row['macd']
        dp.bollinger_upper = row['bollinger_upper']
        dp.bollinger_lower = row['bollinger_lower']
        dp.ma7 = row['ma7']
        dp.atr = row['atr']
        dp.vwap = row['vwap']
        dp.lag1_close = row['lag1_close']
        dp.lag3_close = row['lag3_close']
        dp.log_return = row['log_return']
    
    db.commit()
    logger.info(f"Feature pipeline completed for {len(df)} data points")

