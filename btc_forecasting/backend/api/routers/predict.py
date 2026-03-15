from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas.pydantic_models import PredictionRequest, PredictionResponse
from ..database.db import get_db
from ..models.model_registry import ModelRegistry
from ..database.models import DataPoint
import numpy as np
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=PredictionResponse)
async def predict_next_hour(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """Generate next hour BTC price prediction"""
    try:
        # Load model
        model = ModelRegistry.load_model(request.model_name)
        if not model:
            raise HTTPException(status_code=404, detail=f"Model {request.model_name} not found")
        
        # Prepare features array
        features = np.array(list(request.features.values())).reshape(1, -1)
        
        # Get scaler if available
        scaler = ModelRegistry.load_scaler()
        if scaler:
            features = scaler.transform(features)
        
        # Predict
        prediction = model.predict(features)[0]
        
        return PredictionResponse(
            prediction=float(prediction),
            confidence=0.85,  # Placeholder
            model_version="v1",
            timestamp=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/live")
async def get_live_prediction(db: Session = Depends(get_db)):
    """Get prediction based on latest data"""
    latest = db.query(DataPoint).order_by(DataPoint.timestamp.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No data available")
    
    # Prepare features from latest data point
    features = {
        'rsi': latest.rsi or 0,
        'macd': latest.macd or 0,
        'bollinger_upper': latest.bollinger_upper or 0,
        'bollinger_lower': latest.bollinger_lower or 0,
        'ma7': latest.ma7 or 0,
        'atr': latest.atr or 0,
        'vwap': latest.vwap or 0,
        'lag1_close': latest.lag1_close or latest.close,
        'lag3_close': latest.lag3_close or latest.close,
        'lag6_close': latest.lag6_close or latest.close,
    }
    
    request = PredictionRequest(model_name="LinearRegression", features=features)
    return await predict_next_hour(request, db)

