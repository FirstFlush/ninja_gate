from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from cache.dataclasses import GateActivityData
from street_ninja_common.cache import Seconds
from .enums import RiskProfileStatus, RiskProfileActionSource
from .models import RiskProfile, AbuseEvent


@dataclass
class StatusChangeData:

    profile: RiskProfile
    new_status: RiskProfileStatus
    effective_at: datetime
    source: RiskProfileActionSource
    trigger_event: Optional[AbuseEvent] = None
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None
    
@dataclass
class BaseEvaluationData(ABC):
    
    profile: RiskProfile
    cached_data: GateActivityData


@dataclass
class BaseDecision(ABC):
    
    profile: RiskProfile
    status: RiskProfileStatus
    duration: Optional[Seconds] = None