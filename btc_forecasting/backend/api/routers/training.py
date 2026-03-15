from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from ..schemas.pydantic_models import TrainingResponse
from ..database.db import get_db
from ..tasks.pipelines import train_models
from models.train_linear_regression import train_linear_model
from models.train_arima import train_arima_model

router = APIRouter()

@router.post("/start", response_model=dict)
async def start_training(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Trigger full model training pipeline"""
    background_tasks.add_task(train_models.delay)
    return {"message": "Training pipeline triggered", "status": "queued"}

@router.post("/linear", response_model=TrainingResponse)
async def train_linear(db: Session = Depends(get_db)):
    """Train Linear Regression model synchronously (for testing)"""
    train_linear_model()
    # Get latest model run
    latest = db.query(ModelRun).filter(ModelRun.model_name == "LinearRegression").order_by(ModelRun.created_at.desc()).first()
    if latest:
        return TrainingResponse(
            model_name=latest.model_name,
            rmse=latest.rmse,
            mae=latest.mae,
            directional_accuracy=latest.directional_accuracy,
            mlflow_run_id="latest"  # Would fetch from MLflow
        )
    raise HTTPException(status_code=500, detail="Training failed")

@router.post("/arima", response_model=TrainingResponse)
async def train_arima(db: Session = Depends(get_db)):
    """Train ARIMA model synchronously (for testing)"""
    train_arima_model()
    latest = db.query(ModelRun).filter(ModelRun.model_name == "ARIMA").order_by(ModelRun.created_at.desc()).first()
    if latest:
        return TrainingResponse(
            model_name=latest.model_name,
            rmse=latest.rmse,
            mae=latest.mae,
            directional_accuracy=latest.directional_accuracy,
            mlflow_run_id="latest"
        )
    raise HTTPException(status_code=500, detail="Training failed")

@router.get("/status")
async def training_status(db: Session = Depends(get_db)):
    """Get current model performance"""
    linear = db.query(ModelRun).filter(ModelRun.model_name == "LinearRegression", ModelRun.is_active == True).first()
    arima = db.query(ModelRun).filter(ModelRun.model_name == "ARIMA", ModelRun.is_active == True).first()
    
    return {
        "linear_regression": {
            "rmse": linear.rmse if linear else None,
            "mae": linear.mae if linear else None,
            "accuracy": linear.directional_accuracy if linear else None
        },
        "arima": {
            "rmse": arima.rmse if arima else None,
            "mae": arima.mae if arima else None,
            "accuracy": arima.directional_accuracy if arima else None
        }
    }

