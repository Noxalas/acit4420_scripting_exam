from dataclasses import dataclass


@dataclass
class TransportMode:
    name: str
    kmph: float
    cost: float
    co2_emission: float
