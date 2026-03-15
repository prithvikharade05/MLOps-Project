import numpy as np
import pandas as pd

def psi(expected: pd.Series, actual: pd.Series, bucket_count: int = 10, eps: float = 1e-15) -> float:
    """Standalone PSI calculation"""
    def scale_series(series: pd.Series) -> pd.Series:
        min_val, max_val = series.min(), series.max()
        if max_val == min_val:
            return pd.Series([0.5] * len(series), index=series.index)
        return (series - min_val) / (max_val - min_val)
    
    # Scale to 0-1 range
    expected_scaled = scale_series(expected)
    actual_scaled = scale_series(actual)
    
    # Create buckets
    bucket_edges = np.linspace(0, 1, bucket_count + 1)
    
    expected_buckets, _ = pd.cut(expected_scaled, bins=bucket_edges, retbins=False, duplicates='drop')
    actual_buckets, _ = pd.cut(actual_scaled, bins=bucket_edges, retbins=False, duplicates='drop')
    
    expected_dist = expected_buckets.value_counts(normalize=True).sort_index()
    actual_dist = actual_buckets.value_counts(normalize=True).sort_index()
    
    # Align indices
    all_buckets = expected_dist.index.union(actual_dist.index)
    expected_dist = expected_dist.reindex(all_buckets, fill_value=eps)
    actual_dist = actual_dist.reindex(all_buckets, fill_value=eps)
    
    # Normalize to avoid zero division
    expected_dist /= expected_dist.sum()
    actual_dist /= actual_dist.sum()
    
    psi_value = np.sum((actual_dist - expected_dist) * np.log(actual_dist / expected_dist))
    
    return psi_value

