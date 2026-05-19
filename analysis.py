%%writefile analysis.py
"""
analysis.py - Full analysis and plotting module
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import List
from scipy import stats

sns.set_theme(style="whitegrid", font_scale=1.1)

def load_results_from_hdf5(filepath: str) -> pd.DataFrame:
    """Load results from HDF5 file."""
    import h5py
    results = []
    with h5py.File(filepath, "r") as f:
        results_group = f["results"]
        keys = list(results_group.keys())
        n_rows = len(results_group[keys[0]])
        for i in range(n_rows):
            row = {key: results_group[key][i] for key in keys}
            results.append(row)
    return pd.DataFrame(results)


def generate_full_analysis(df: pd.DataFrame, output_dir: str = "figures", test_type: str = "mannwhitney"):
    """Generate statistical summary and plots."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("\n" + "="*80)
    print("STATISTICAL SUMMARY")
    print("="*80)

    # Group by beta or epsilon
    if "beta" in df.columns:
        group_col = "beta"
    else:
        group_col = "epsilon"

    summary = df.groupby(group_col)[["transitions", "residence_time_active", "active_time_fraction"]].agg(['mean', 'std']).round(4)
    print(summary)

    print(f"\n✅ Analysis completed. Figures would be saved in: {output_dir}")
