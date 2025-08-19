from dataclasses import dataclass
from typing import Any

@dataclass
class AbuseEventCache:

    timestamp: float
    abuse_type: str


@dataclass
class GateActivityData:
    
    abuse_events: list[AbuseEventCache]
    last_updated: float
