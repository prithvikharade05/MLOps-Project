import mlflow
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from sqlalchemy.orm import Session
from database.models import DataPoint, ModelRun
from database.db import get_db
from utils.config import settings
import logging
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
mlflow.set_experiment("btc_forecasting_arima")

def prepare_arima_data(db: Session) -> pd.Series:
    """Prepare univariate time series for ARIMA"""
    data = db.query(DataPoint.timestamp, DataPoint.log_return).order_by(DataPoint.timestamp).all()
    
    df = pd.DataFrame(data, columns=['timestamp', 'log_return'])
    df.set_index('timestamp', inplace=True)
    
    return df['log_return'].dropna()

def train_arima_model():
    """Train ARIMA model with MLflow tracking"""
    db = next(get_db())
    
    try:
        series = prepare_arima_data(db)
        if len(series) < 50:
            raise ValueError("Not enough data for ARIMA training")
        
        with mlflow.start_run():
            # ARIMA parameters
            order = (5, 1, 0)  # ARIMA(5,1,0)
            
            mlflow.log_param("model_type", "ARIMA")
            mlflow.log_param("order_p", order[0])
            mlflow.log_param("order_d", order[1])
            mlflow.log_param("order_q", order[2])
            
            # Train model
            model = ARIMA(series, order=order)
            fitted_model = model.fit()
            
            # Forecast next hour
            forecast = fitted_model.forecast(steps=1)
            
            # In-sample metrics
            y_pred = fitted_model.fittedvalues
            rmse = np.sqrt(((series - y_pred) ** 2).mean())
            mae = np.mean(np.abs(series - y_pred))
            directional_accuracy = np.mean(np.sign(series.diff()) == np.sign(y_pred.diff())) * 100
            
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("directional_accuracy", directional_accuracy)
            
            logger.info(f"ARIMA RMSE: {rmse:.6f}, MAE: {mae:.6f}, Directional Accuracy: {directional_accuracy:.2f}%")
            
            # Log model
            mlflow.statsmodels.log_model(fitted_model, "arima_model")
            
            # Register model
            model_uri = mlflow.statsmodels.log_model(fitted_model, "arima_model").model_uri
            mlflow.register_model(model_uri, "ARIMA")
            
            # Save to DB
            model_run = ModelRun(
                model_name="ARIMA",
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
    train_arima_model()

