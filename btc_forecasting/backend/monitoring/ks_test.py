from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from typing import Dict, List

class KSTestMonitor:
    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha
    
    def run_ks_test(self, reference_data: pd.Series, current_data: pd.Series) -> Dict[str, float]:
        """Run KS test between reference and current data"""
        if len(reference_data) < 10 or len(current_data) < 10:
            return {"ks_statistic": 0.0, "p_value": 1.0, "rejected": False}
        
        stat, p_value = ks_2samp(reference_data.dropna(), current_data.dropna())
        
        rejected = p_value < self.alpha
        
        return {
            "ks_statistic": stat,
            "p_value": p_value,
            "rejected": rejected,
            "alpha": self.alpha
        }
    
    def batch_ks_test(self, reference_df: pd.DataFrame, current_df: pd.DataFrame, features: List[str]) -> Dict[str, dict]:
        """Run KS test on multiple features"""
        results = {}
        for feature in features:
            results[feature] = self.run_ks_test(
                reference_df[feature], 
                current_df[feature]
            )
        return results

