import pandas as pd
from typing import Dict, Any


def compute_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_columns:
        return {}

    statistics = {}

    for column in numeric_columns:
        data = df[column].dropna()
        if data.empty:
            continue

        statistics[column] = {
            "count": int(data.count()),
            "mean": float(data.mean()),
            "median": float(data.median()),
            "std": float(data.std()),
            "min": float(data.min()),
            "max": float(data.max()),
        }

    return statistics
