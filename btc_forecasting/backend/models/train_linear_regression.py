import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database.models import DataPoint, ModelRun
from database.db import get_db
from utils.config import settings
import logging
import joblib

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_experiment("btc_forecasting_linear")

FEATURES = [
    'rsi', 'macd', 'bollinger_upper', 'bollinger_lower', 'ma7', 
    'atr', 'vwap', 'lag1_close', 'lag3_close', 'lag6_close',
    'rolling_mean_20', 'rolling_std_20', 'volatility'
]

def prepare_data(db: Session) -> tuple:
    """Prepare training data from database"""
    data = db.query(DataPoint).order_by(DataPoint.timestamp).all()
    if len(data) < 100:
        raise ValueError("Not enough data for training")
    
    df = pd.DataFrame([{
        'rsi': d.rsi, 'macd': d.macd, 'bollinger_upper': d.bollinger_upper,
        'bollinger_lower': d.bollinger_lower, 'ma7': d.ma7, 'atr': d.atr,
        'vwap': d.vwap, 'lag1_close': d.lag1_close, 'lag3_close': d.lag3_close,
        'rolling_mean_20': d.rolling_mean_20 if hasattr(d, 'rolling_mean_20') else 0,
        'rolling_std_20': d.rolling_std_20 if hasattr(d, 'rolling_std_20') else 0,
        'volatility': d.volatility if hasattr(d, 'volatility') else 0,
        'log_return': d.log_return
    } for d in data if d.log_return is not None])
    
    df = df.dropna()
    X = df[FEATURES]
    y = df['log_return']
    
    return X, y

def train_linear_model():
    """Train Linear Regression model with MLflow tracking"""
    db = next(get_db())
    
    try:
        X, y = prepare_data(db)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        with mlflow.start_run():
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            mlflow.log_param("model_type", "LinearRegression")
            mlflow.log_param("features", FEATURES)
            mlflow.log_param("train_size", len(X_train))
            mlflow.log_param("test_size", len(X_test))
            
            # Train model
            model = LinearRegression()
            model.fit(X_train_scaled, y_train)
            
            # Predictions
            y_pred = model.predict(X_test_scaled)
            
            # Metrics
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = mean_absolute_error(y_test, y_pred)
            directional_accuracy = np.mean(np.sign(y_test) == np.sign(y_pred)) * 100
            
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("directional_accuracy", directional_accuracy)
            
            logger.info(f"RMSE: {rmse:.6f}, MAE: {mae:.6f}, Directional Accuracy: {directional_accuracy:.2f}%")
            
            # Log model and scaler
            mlflow.sklearn.log_model(model, "model")
            joblib.dump(scaler, "scaler.pkl")
            mlflow.log_artifact("scaler.pkl")
            
            # Register model
            model_uri = mlflow.sklearn.log_model(model, "model").model_uri
            mlflow.register_model(model_uri, "LinearRegression")
            
            # Save to DB
            model_run = ModelRun(
                model_name="LinearRegression",
                version="v1",
                rmse=rmse,
                mae=mae,
                directional_accuracy=directional_accuracy,
                is_active=True
            )
            db.add(model_run)
            db.commit()
            
    finally:
        db.close()

if __name__ == "__main__":
    train_linear_model()

