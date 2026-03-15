from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import math

class OHLCV(BaseModel):
    timestamp: datetime
    open: float = Field(..., ge=0)
    high: float = Field(..., ge=0)
    low: float = Field(..., ge=0)
    close: float = Field(..., ge=0)
    volume: float = Field(..., ge=0)

class PredictionRequest(BaseModel):
    model_name: str = Field(..., description="LinearRegression or ARIMA")
    features: Dict[str, float]

class PredictionResponse(BaseModel):
    prediction: float = Field(..., description="Next hour log return forecast")
    confidence: Optional[float] = Field(None, description="Prediction confidence")
    model_version: str
    timestamp: datetime = Field(default_factory=datetime.now)

class TrainingResponse(BaseModel):
    model_name: str
    rmse: float
    mae: float
    directional_accuracy: float
    mlflow_run_id: str

class DriftReport(BaseModel):
    feature: str
    psi: float
    ks_statistic: float
    ks_p_value: float
    alert_level: str
    drift_detected: bool

class HealthCheck(BaseModel):
    status: str
    database: str

class PipelineStatus(BaseModel):
    message: str
    status: str

