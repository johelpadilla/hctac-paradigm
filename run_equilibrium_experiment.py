%%writefile run_equilibrium_experiment.py
"""
run_equilibrium_experiment.py
EXPERIMENTO 1 REAL - Characterization of Equilibria (Full Version)
"""

import numpy as np
from equilibrium_experiment import EquilibriumExperiment
from data_manager import DataManager
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    logger = logging.getLogger(__name__)

    logger.info("="*70)
    logger.info("EXPERIMENTO 1 REAL - Characterization of Equilibria (HCT-AC v2.3)")
    logger.info("="*70)

    system_params = {
        "N": 100,
        "r": 4.0
    }

    protocol_params = {
        "tau_ign": 0.50,
        "tau_sat": 0.92,
        "min_persistence": 5,
        "hysteresis_duration": 30
    }

    # Parámetros reales
    epsilons = np.round(np.arange(0.10, 0.96, 0.05), 2).tolist()

    experiment = EquilibriumExperiment(
        system_params=system_params,
        protocol_params=protocol_params,
        n_replicas=8,           # Versión real (balance entre calidad y tiempo)
        use_saturation=True,
        seed_base=42
    )

    experiment.run(epsilons=epsilons)

    # Guardar resultados
    data_manager = DataManager(
        base_path="results/experiments",
        experiment_name="equilibrium_full_v2_3"
    )

    metadata = {
        "protocol_version": "v2.3",
        "experiment_type": "Full Equilibrium Characterization",
        "n_replicas": 8,
        "epsilons_tested": len(epsilons),
        "use_saturation": True
    }

    data_manager.save_results(results=experiment.results, metadata=metadata)

    logger.info("EXPERIMENTO 1 REAL FINALIZADO EXITOSAMENTE")


if __name__ == "__main__":
    main()
