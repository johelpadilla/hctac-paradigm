%%writefile data_manager.py
"""
data_manager.py - Professional data saving for experiments
"""

import h5py
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class DataManager:
    """
    Manages saving experiment results in HDF5 format with metadata.
    """

    def __init__(self, base_path: str = "results", experiment_name: str = "experiment"):
        self.base_path = Path(base_path)
        self.experiment_name = experiment_name
        self.experiment_path = self.base_path / experiment_name
        self.experiment_path.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{experiment_name}_{self.timestamp}"

    def save_results(self, results: list, metadata: Optional[Dict[str, Any]] = None):
        """Save results to HDF5 file with metadata."""
        filename = self.experiment_path / f"{self.run_id}.h5"

        with h5py.File(filename, "w") as f:
            # Save results
            results_group = f.create_group("results")
            for key in results[0].keys():
                data = [r.get(key) for r in results]
                results_group.create_dataset(key, data=data)

            # Save metadata
            meta_group = f.create_group("metadata")
            meta_group.attrs["run_id"] = self.run_id
            meta_group.attrs["timestamp"] = self.timestamp
            meta_group.attrs["experiment_name"] = self.experiment_name

            if metadata:
                for key, value in metadata.items():
                    if isinstance(value, (dict, list)):
                        meta_group.attrs[key] = json.dumps(value)
                    else:
                        meta_group.attrs[key] = str(value)

        print(f"✅ Results saved successfully: {filename}")
