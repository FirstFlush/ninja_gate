from dataclasses import dataclass
from datetime import datetime
from typing import NewType

UnixTimestamp = NewType("UnixTimestamp", float)

@dataclass
class GateActivityData:
    valid_msgs: list[UnixTimestamp]
    invalid_msgs: list[UnixTimestamp]
    last_updated: UnixTimestamp
    
    