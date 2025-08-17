from dataclasses import dataclass


@dataclass
class GateActivityData:
    valid_msgs: list[float]
    invalid_msgs: list[float]
    last_updated: float