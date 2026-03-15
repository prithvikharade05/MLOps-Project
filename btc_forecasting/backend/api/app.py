from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database.db import get_db, engine, Base
from database.models import DataPoint, ModelRun, DriftAlert
from utils.config import settings
from tasks.pipelines import full_pipeline, hourly_pipeline
from models.model_registry import ModelRegistry
import uvicorn
import logging
from routers import predict, training, monitoring, metrics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting BTC Forecasting API...")
    yield
    logger.info("Shutting down BTC Forecasting API...")

app = FastAPI(
    title="BTC Forecasting MLOps Platform",
    description="Production-grade Bitcoin forecasting with full MLOps pipeline",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router, prefix="/api/v1/predict", tags=["predictions"])
app.include_router(training.router, prefix="/api/v1/training", tags=["training"])
app.include_router(monitoring.router, prefix="/api/v1/monitoring", tags=["monitoring"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["metrics"])

@app.get("/")
async def root():
    return {"message": "BTC Forecasting MLOps Platform", "status": "operational"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test DB connection
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pipeline/full")
async def trigger_full_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(full_pipeline.delay)
    return {"message": "Full pipeline triggered", "status": "queued"}

@app.post("/pipeline/hourly")
async def trigger_hourly_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(hourly_pipeline.delay)
    return {"message": "Hourly pipeline triggered", "status": "queued"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

