%%writefile noise_intermittency_experiment.py
"""
noise_intermittency_experiment.py
EXPERIMENT 3 - Noise and Intermittency (Full Real Version)
"""

import numpy as np
from typing import List, Dict
from datetime import datetime
from coupled_map_lattice import CoupledMapLattice
from hctac_protocol_v2_3 import HCTACProtocol_v2_3
from utils import detect_transitions, calculate_residence_times

class NoiseIntermittencyExperiment:
    """
    Experiment 3: Full version - Effect of Noise and Intermittency (HCT-AC v2.3)
    """

    def __init__(self,
                 system_params: dict,
                 protocol_params: dict,
                 noise_levels: List[float],
                 n_replicas: int = 10,
                 use_saturation: bool = True,
                 total_steps: int = 30000,
                 seed_base: int = 42):

        self.system_params = system_params
        self.protocol_params = protocol_params
        self.noise_levels = noise_levels
        self.n_replicas = n_replicas
        self.use_saturation = use_saturation
        self.total_steps = total_steps
        self.seed_base = seed_base
        self.results: List[Dict] = []

    def run(self):
        print(f"Starting full Noise & Intermittency Experiment")
        print(f"Noise levels: {self.noise_levels} | Replicas per level: {self.n_replicas}\n")

        for beta in self.noise_levels:
            for rep in range(self.n_replicas):
                seed = self.seed_base + rep + int(beta * 1000)
                result = self._run_single_replica(beta=beta, replica=rep, seed=seed)
                self.results.append(result)

        print(f"Experiment 3 finished. Total results: {len(self.results)}")

    def _run_single_replica(self, beta: float, replica: int, seed: int) -> Dict:
        system = CoupledMapLattice(
            N=self.system_params.get("N", 100),
            epsilon=self.system_params.get("epsilon", 0.60),
            seed=seed
        )
        protocol = HCTACProtocol_v2_3(
            **self.protocol_params,
            use_saturation=self.use_saturation
        )

        # Phase 1: Passive equilibrium
        system.evolve(steps=8000)

        # Phase 2: Run with noise
        tick_history = []
        tau_history = []

        for _ in range(self.total_steps):
            system.step_and_record()
            tau_g = system.get_tau_g(history_length=40)
            tick_registered = protocol.update(tau_g)

            tick_history.append(1 if tick_registered else 0)
            tau_history.append(tau_g)

        # Analysis
        transitions, regime_series = detect_transitions(tick_history, window=50)
        residence_active, residence_inactive = calculate_residence_times(regime_series)
        active_fraction = sum(regime_series) / len(regime_series)

        return {
            "beta": beta,
            "replica": replica,
            "seed": seed,
            "use_saturation": self.use_saturation,
            "transitions": transitions,
            "residence_time_active": residence_active,
            "residence_time_inactive": residence_inactive,
            "active_time_fraction": active_fraction,
            "mean_tau": np.mean(tau_history),
            "tau_variance": np.var(tau_history),
            "timestamp": datetime.now().isoformat()
        }
