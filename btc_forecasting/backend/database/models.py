from sqlalchemy import Column, Integer, Float, DateTime, String, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from database.db import Base

class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    
    # Features
    rsi = Column(Float)
    macd = Column(Float)
    bollinger_upper = Column(Float)
    bollinger_lower = Column(Float)
    ma7 = Column(Float)
    ma21 = Column(Float)
    atr = Column(Float)
    vwap = Column(Float)
    log_return = Column(Float)

    # Lags
    lag1_close = Column(Float)
    lag3_close = Column(Float)
    lag6_close = Column(Float)

    __table_args__ = (Index('ix_data_points_timestamp', 'timestamp'),)

class ModelRun(Base):
    __tablename__ = "model_runs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True)
    version = Column(String)
    rmse = Column(Float)
    mae = Column(Float)
    directional_accuracy = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class DriftAlert(Base):
    __tablename__ = "drift_alerts"

    id = Column(Integer, primary_key=True, index=True)
    feature_name = Column(String, index=True)
    psi_value = Column(Float)
    ks_statistic = Column(Float)
    alert_level = Column(String)  # 'low', 'medium', 'high'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

