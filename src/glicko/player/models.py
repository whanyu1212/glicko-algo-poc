from dataclasses import dataclass


@dataclass
class Player:
    name: str
    R: float
    RD: float
    σ: float
    μ: float
    φ: float
