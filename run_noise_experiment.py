%%writefile run_noise_experiment.py
"""
run_noise_experiment.py
EXPERIMENTO 3 REAL - Noise and Intermittency (Full Version)
"""

import numpy as np
from noise_intermittency_experiment import NoiseIntermittencyExperiment
from data_manager import DataManager
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("="*70)
    logger.info("EXPERIMENTO 3 REAL - Noise & Intermittency (HCT-AC v2.3)")
    logger.info("="*70)

    system_params = {
        "N": 100,
        "epsilon": 0.60
    }

    protocol_params = {
        "tau_ign": 0.50,
        "tau_sat": 0.92,
        "min_persistence": 5,
        "hysteresis_duration": 30
    }

    noise_levels = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25]

    experiment = NoiseIntermittencyExperiment(
        system_params=system_params,
        protocol_params=protocol_params,
        noise_levels=noise_levels,
        n_replicas=8,              # Versión real
        use_saturation=True,
        total_steps=25000,         # Versión real
        seed_base=42
    )

    experiment.run()

    # Guardar resultados
    data_manager = DataManager(
        base_path="results/experiments",
        experiment_name="noise_intermittency_full_v2_3"
    )

    metadata = {
        "protocol_version": "v2.3",
        "experiment_type": "Full Noise & Intermittency Study",
        "n_replicas": 8,
        "noise_levels_tested": len(noise_levels),
        "use_saturation": True
    }

    data_manager.save_results(results=experiment.results, metadata=metadata)

    logger.info("EXPERIMENTO 3 REAL FINALIZADO EXITOSAMENTE")


if __name__ == "__main__":
    main()
