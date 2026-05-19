%%writefile utils.py
"""
utils.py - Helper functions for experiments
"""

import numpy as np
from typing import List, Tuple

def detect_transitions(tick_history: List[int], window: int = 50) -> Tuple[int, List[int]]:
    """Detect transitions between active and inactive regimes."""
    n = len(tick_history)
    regime_series = [0] * n

    for i in range(n):
        start = max(0, i - window + 1)
        recent_activity = sum(tick_history[start:i + 1])
        regime_series[i] = 1 if recent_activity > 0 else 0

    transitions = sum(1 for i in range(1, n) if regime_series[i] != regime_series[i - 1])
    return transitions, regime_series


def calculate_residence_times(regime_series: List[int]) -> Tuple[float, float]:
    """Calculate average residence time in active and inactive regimes."""
    if not regime_series:
        return 0.0, 0.0

    active_durations = []
    inactive_durations = []
    current_duration = 1
    current_state = regime_series[0]

    for i in range(1, len(regime_series)):
        if regime_series[i] == current_state:
            current_duration += 1
        else:
            if current_state == 1:
                active_durations.append(current_duration)
            else:
                inactive_durations.append(current_duration)
            current_state = regime_series[i]
            current_duration = 1

    if current_state == 1:
        active_durations.append(current_duration)
    else:
        inactive_durations.append(current_duration)

    mean_active = float(np.mean(active_durations)) if active_durations else 0.0
    mean_inactive = float(np.mean(inactive_durations)) if inactive_durations else 0.0

    return mean_active, mean_inactive
