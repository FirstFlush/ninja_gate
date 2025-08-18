from dataclasses import dataclass
from typing import Any, Optional
from gatekeeper.enums import AbuseEventTypeEnum 
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
    phone_number: str
    msg: str
    parsed_number: PhoneNumber