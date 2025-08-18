from dataclasses import dataclass


@dataclass
class GateActivityData:
    
    invalid_msgs: list[float]
    last_updated: float