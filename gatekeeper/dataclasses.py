from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from django.db.models import QuerySet
from typing import Optional
from cache.dataclasses import GateActivityData
from street_ninja_common.cache import Seconds
from .enums import RiskProfileStatus, RiskProfileActionSource
from .models import RiskProfile, AbuseEvent


@dataclass
class RiskProfileActionData:

    profile: RiskProfile
    status: RiskProfileStatus
    source: RiskProfileActionSource
    trigger_event: Optional[AbuseEvent] = None
    expiry: Optional[datetime] = None
    notes: Optional[str] = None

@dataclass
class EvaluationData(ABC):
    
    profile: RiskProfile
    cached_data: GateActivityData
    msg: str
    
@dataclass
class PreflightEvaluationData(EvaluationData):

    current_events: QuerySet[AbuseEvent]