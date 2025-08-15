from dataclasses import dataclass
from datetime import datetime
from typing import Optional
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