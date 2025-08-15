from dataclasses import dataclass
from gatekeeper.enums import AbuseEventTypeEnum 


@dataclass
class DetectedAbuseEvent:
    method_name: str
    abuse_event_type: AbuseEventTypeEnum
    
