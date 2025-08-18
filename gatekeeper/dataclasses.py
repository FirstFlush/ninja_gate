from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from cache.dataclasses import GateActivityData
from .enums import RiskProfileStatus
from .models import RiskProfile, AbuseEvent


@dataclass
class StatusChangeData:

    profile: RiskProfile
    new_status: RiskProfileStatus
    effective_at: datetime
    trigger_event: Optional[AbuseEvent] = None
    expires_at: Optional[datetime] = None
    notes: Optional[str] = None
    
@dataclass
class BaseEvaluationData(ABC):
    
    profile: RiskProfile
    cached_data: GateActivityData


@dataclass
class BaseEvaluationDecision(ABC):
    
    profile: RiskProfile
    status: RiskProfileStatus