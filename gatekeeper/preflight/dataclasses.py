from dataclasses import dataclass
from django.db.models import QuerySet
from typing import Any, Optional
from .enums import RequestAction
from ..dataclasses import BaseEvaluationData, BaseDecision
from ..enums import AbuseEventTypeEnum 
from ..models import RiskProfile, AbuseEvent
from phonenumbers import PhoneNumber

@dataclass
class DetectedAbuseEvent:
    abuse_event_type: AbuseEventTypeEnum
    context: Optional[dict[str, Any]] = None

@dataclass
class DetectedAbuseEvents:
    events: list[DetectedAbuseEvent]
    sms_id: int
    msg: str

@dataclass
class ScreeningCheckData:
    profile: RiskProfile
    phone_number: str
    msg: str
    parsed_number: PhoneNumber
    

@dataclass
class PreflightEvaluationData(BaseEvaluationData):
    
    abuse_events: QuerySet[AbuseEvent]
    

@dataclass
class PreflightDecision(BaseDecision):

    action = RequestAction
