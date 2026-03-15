from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
import pandas as pd
from sqlalchemy.orm import Session
from database.models import DataPoint
from database.db import get_db
from utils.config import settings
import mlflow
import numpy as np
import logging

logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

def calculate_psi(reference: pd.Series, current: pd.Series, buckets=10) -> float:
    """Calculate Population Stability Index"""
    def scale_range(input_data, min_val, max_val):
        return (input_data - min_val) / (max_val - min_val)
    
    def get_bucket_ranges(data, n_buckets):
        data = scale_range(data, data.min(), data.max())
        buckets = np.linspace(0, 1, n_buckets + 1)
        return buckets
    
    cut = pd.cut(current, bins=get_bucket_ranges(reference, buckets), include_lowest=True)
    e1 = current.groupby(cut).count() / len(current)
    cut = pd.cut(reference, bins=get_bucket_ranges(reference, buckets), include_lowest=True)
    e2 = reference.groupby(cut).count() / len(reference)
    
    psi = np.sum((e1 - e2) * np.log(e1 / e2))
    return psi

def ks_test(reference: pd.Series, current: pd.Series) -> tuple:
    """Kolmogorov-Smirnov test"""
    from scipy.stats import ks_2samp
    stat, p_value = ks_2samp(reference, current)
    return stat, p_value

def generate_drift_report(db: Session, feature_name: str, reference_period_days: int = 30) -> dict:
    """Generate drift report for a specific feature"""
    # Reference data (older)
    ref_end = pd.Timestamp.now() - pd.Timedelta(days=reference_period_days * 2)
    ref_start = ref_end - pd.Timedelta(days=reference_period_days)
    
    # Current data (recent)
    current_start = ref_end
    current_end = pd.Timestamp.now()
    
    ref_data = db.query(getattr(DataPoint, feature_name)) \
        .filter(DataPoint.timestamp >= ref_start, DataPoint.timestamp <= ref_end) \
        .all()
    
    current_data = db.query(getattr(DataPoint, feature_name)) \
        .filter(DataPoint.timestamp >= current_start, DataPoint.timestamp <= current_end) \
        .all()
    
    if not ref_data or not current_data:
        return {"error": "Insufficient data"}
    
    ref_values = pd.Series([getattr(d, feature_name) for d in ref_data if getattr(d, feature_name) is not None])
    current_values = pd.Series([getattr(d, feature_name) for d in current_data if getattr(d, feature_name) is not None])
    
    psi = calculate_psi(ref_values, current_values)
    ks_stat, ks_p = ks_test(ref_values, current_values)
    
    alert_level = "low" if psi < 0.1 else "medium" if psi < 0.2 else "high"
    
    with mlflow.start_run():
        mlflow.log_metric(f"{feature_name}_psi", psi)
        mlflow.log_metric(f"{feature_name}_ks_stat", ks_stat)
        mlflow.log_metric(f"{feature_name}_ks_pvalue", ks_p)
    
    return {
        "feature": feature_name,
        "psi": psi,
        "ks_statistic": ks_stat,
        "ks_p_value": ks_p,
        "alert_level": alert_level,
        "drift_detected": psi > 0.2
    }

