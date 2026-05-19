%%writefile coupled_map_lattice.py
import numpy as np
from typing import Optional
from scipy.stats import spearmanr

class CoupledMapLattice:
    """
    Coupled Map Lattice with Systemic Tau calculation (Full Version)
    """

    def __init__(self, N: int, epsilon: float, r: float = 4.0, seed: Optional[int] = None):
        if not (0 <= epsilon <= 1):
            raise ValueError("epsilon must be between 0 and 1")

        self.N = N
        self.epsilon = epsilon
        self.r = r
        self.seed = seed
        self.state = np.zeros(N)
        self._rng = np.random.default_rng(seed)
        self._history = []
        self._initialize_state()

    def _initialize_state(self):
        self.state = self._rng.uniform(0, 1, self.N)

    def step(self):
        new_state = np.zeros(self.N)
        for i in range(self.N):
            left = self.state[(i - 1) % self.N]
            right = self.state[(i + 1) % self.N]
            coupled = (1 - self.epsilon) * self.state[i] + (self.epsilon / 2) * (left + right)
            new_state[i] = self.r * coupled * (1 - coupled)
        self.state = new_state

    def step_and_record(self):
        self.step()
        self._history.append(self.state.copy())
        if len(self._history) > 200:
            self._history.pop(0)

    def evolve(self, steps: int):
        for _ in range(steps):
            self.step_and_record()

    def get_tau_g(self, history_length: int = 50) -> float:
        if len(self._history) < history_length:
            return 0.45
        recent_history = np.array(self._history[-history_length:])
        correlations = []
        for i in range(self.N):
            for j in range(i + 1, self.N):
                rho, _ = spearmanr(recent_history[:, i], recent_history[:, j])
                correlations.append(rho)
        return np.mean(correlations) if correlations else 0.45

    def get_state(self) -> np.ndarray:
        return self.state.copy()
