from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerRanges:
    """Configuration constants for player rating ranges."""

    r_min: float = 1000
    r_max: float = 8000
    rd_min: float = 200
    rd_max: float = 1000
    sigma_min: float = 0.1
    sigma_max: float = 1.0
    glicko_constant: float = 173.7178
