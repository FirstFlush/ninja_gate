from dataclasses import dataclass
from datetime import datetime
from typing import NewType

# UnixTimestamp = NewType("UnixTimestamp", float)

@dataclass
class GateActivityData:
    valid_msgs: list[float]
    invalid_msgs: list[float]
    last_updated: float