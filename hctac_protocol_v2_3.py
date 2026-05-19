%%writefile hctac_protocol_v2_3.py
"""
HCT-AC Protocol v2.3 - Full Version
"""

from typing import Optional

class HCTACProtocol_v2_3:
    """
    Hierarchical Causal Tick & Adaptive Coherence Protocol v2.3
    """

    def __init__(self,
                 tau_ign: float = 0.50,
                 tau_sat: float = 0.92,
                 min_persistence: int = 5,
                 hysteresis_duration: int = 30,
                 use_saturation: bool = True):
        
        self.tau_ign = tau_ign
        self.tau_sat = tau_sat
        self.min_persistence = min_persistence
        self.hysteresis_duration = hysteresis_duration
        self.use_saturation = use_saturation

        # Internal state
        self.persistence_counter = 0
        self.hysteresis_counter = 0
        self.tick_count = 0
        self.in_hysteresis = False

    def update(self, tau_g: float) -> bool:
        """Update protocol and return True if a valid tick was registered."""
        tick_registered = False

        if tau_g >= self.tau_ign:
            self.persistence_counter += 1
        else:
            self.persistence_counter = 0

        if self.persistence_counter >= self.min_persistence:
            self.tick_count += 1
            tick_registered = True
            self.persistence_counter = 0
            self.hysteresis_counter = self.hysteresis_duration
            self.in_hysteresis = True

        if self.in_hysteresis:
            self.hysteresis_counter -= 1
            if self.hysteresis_counter <= 0:
                self.in_hysteresis = False

        return tick_registered

    def reset(self):
        """Reset protocol state."""
        self.persistence_counter = 0
        self.hysteresis_counter = 0
        self.tick_count = 0
        self.in_hysteresis = False
