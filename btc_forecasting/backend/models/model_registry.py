import mlflow
import mlflow.sklearn
import mlflow.statsmodels
from utils.config import settings
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

class ModelRegistry:
    @staticmethod
    def load_model(model_name: str, stage: str = "Production") -> Optional[Any]:
        """Load registered model from MLflow"""
        try:
            model_uri = f"models:/{model_name}/{stage}"
            model = mlflow.pyfunc.load_model(model_uri)
            logger.info(f"Loaded model {model_name} from stage {stage}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {str(e)}")
            return None
    
    @staticmethod
    def load_scaler(experiment_name: str = "btc_forecasting_linear") -> Optional[Any]:
        """Load scaler artifact from latest run"""
        try:
            runs = mlflow.search_runs(experiment_ids=[mlflow.get_experiment_by_name(experiment_name).experiment_id])
            if runs.empty:
                return None
            
            latest_run = runs.loc[runs['start_time'].idxmax()]
            scaler_path = f"runs:/{latest_run['run_id']}/scaler.pkl"
            scaler = mlflow.pyfunc.load_model(scaler_path)
            return scaler
        except Exception as e:
            logger.error(f"Failed to load scaler: {str(e)}")
            return None
    
    @staticmethod
    def promote_model(model_name: str, from_stage: str, to_stage: str):
        """Promote model between stages"""
        try:
            client = mlflow.MlflowClient()
            client.transition_model_version_stage(
                name=model_name,
                version=client.get_latest_versions(model_name, stages=[from_stage])[0].version,
                stage=to_stage
            )
            logger.info(f"Promoted {model_name} from {from_stage} to {to_stage}")
        except Exception as e:
            logger.error(f"Failed to promote model: {str(e)}")

