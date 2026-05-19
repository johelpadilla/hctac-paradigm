%%writefile equilibrium_experiment.py
"""
equilibrium_experiment.py
EXPERIMENT 1 - Characterization of Equilibria (Full Version)
"""

import numpy as np
from typing import List, Dict
from datetime import datetime
from coupled_map_lattice import CoupledMapLattice
from hctac_protocol_v2_3 import HCTACProtocol_v2_3

class EquilibriumExperiment:
    """
    Experiment 1: Full Characterization of Equilibria (HCT-AC v2.3)
    """

    def __init__(self, system_params: dict, protocol_params: dict,
                 n_replicas: int = 10, use_saturation: bool = True, seed_base: int = 42):

        self.system_params = system_params
        self.protocol_params = protocol_params
        self.n_replicas = n_replicas
        self.use_saturation = use_saturation
        self.seed_base = seed_base
        self.results: List[Dict] = []

    def run(self, epsilons: List[float]):
        """Run the full experiment."""
        print(f"Starting Equilibrium Experiment with {len(epsilons)} epsilon values and {self.n_replicas} replicas.")

        for eps in epsilons:
            for rep in range(self.n_replicas):
                seed = self.seed_base + rep + int(eps * 100)
                result = self._run_single_replica(epsilon=eps, replica=rep, seed=seed)
                self.results.append(result)

        print(f"Experiment 1 finished. Total results: {len(self.results)}")

    def _run_single_replica(self, epsilon: float, replica: int, seed: int) -> Dict:
        system = CoupledMapLattice(N=self.system_params['N'], epsilon=epsilon, seed=seed)
        protocol = HCTACProtocol_v2_3(**self.protocol_params, use_saturation=self.use_saturation)

        # Phase 1: Type A (No ticks)
        system.evolve(steps=8000)
        tau_A_mean, tau_A_std = self._measure_tau(system, window=4000)

        # Phase 2: Active equilibrium
        protocol.reset()
        system.evolve(steps=15000)
        tau_B_mean, tau_B_std, tick_rate, sat_fraction, tau_values = self._measure_steady_state(system, protocol)

        equilibrium_type = self._classify_equilibrium(tau_B_mean, tick_rate, sat_fraction)

        # Phase 3: Perturbation test
        pert_neg = self._test_perturbation(system, protocol, direction=-0.15)
        pert_pos = self._test_perturbation(system, protocol, direction=+0.10)

        return {
            "epsilon": epsilon,
            "replica": replica,
            "seed": seed,
            "use_saturation": self.use_saturation,
            "tau_A_mean": tau_A_mean,
            "tau_A_std": tau_A_std,
            "tau_B_mean": tau_B_mean,
            "tau_B_std": tau_B_std,
            "tau_B_variance": np.var(tau_values),
            "tick_rate": tick_rate,
            "saturation_time_fraction": sat_fraction,
            "equilibrium_type": equilibrium_type,
            "perturbation_negative": pert_neg,
            "perturbation_positive": pert_pos,
            "timestamp": datetime.now().isoformat()
        }

    def _classify_equilibrium(self, tau_mean: float, tick_rate: float, sat_fraction: float) -> str:
        if tick_rate < 0.001:
            return "Type_A_No_Ticks"
        elif tau_mean < self.protocol_params.get("tau_sat", 0.92):
            return "Type_B_Sustained_Ticks"
        else:
            return "Type_C_High_Coherence_Saturated"

    def _measure_tau(self, system, window=4000):
        taus = [system.get_tau_g() for _ in range(window)]
        return np.mean(taus), np.std(taus)

    def _measure_steady_state(self, system, protocol):
        taus, ticks, sat_steps = [], 0, 0
        for _ in range(8000):
            system.step_and_record()
            tau_g = system.get_tau_g()
            taus.append(tau_g)
            if protocol.update(tau_g):
                ticks += 1
            if tau_g > protocol.tau_sat:
                sat_steps += 1
        return np.mean(taus), np.std(taus), ticks / 8000, sat_steps / 8000, taus

    def _test_perturbation(self, system, protocol, direction, duration=100):
        pre_tau = system.get_tau_g(history_length=30)
        original_state = system.get_state().copy()
        noise = np.random.normal(0, 0.08, size=system.N)
        perturbed_state = np.clip(original_state + direction * noise, 0, 1)
        system.state = perturbed_state

        ticks_during = 0
        for _ in range(duration):
            system.step_and_record()
            tau_g = system.get_tau_g(history_length=30)
            if protocol.update(tau_g):
                ticks_during += 1

        post_tau = system.get_tau_g(history_length=30)
        tau_diff = abs(post_tau - pre_tau)
        recovered = (tau_diff < 0.08) and (ticks_during > 2)

        return {
            "pre_tau": round(pre_tau, 4),
            "post_tau": round(post_tau, 4),
            "tau_difference": round(tau_diff, 4),
            "recovered": recovered,
            "ticks_during": ticks_during,
            "direction": direction
        }
