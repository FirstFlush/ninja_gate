import logging
from django.db import IntegrityError, DatabaseError
from django.utils import timezone
from gatekeeper.enums import AbuseEventSourceEnum
from ..schemas import PreflightRequestData
from .abuse_detection import AbuseDetectionService
from .abuse_event import AbuseEventService
from ..dataclasses import DetectedAbuseEvent, DetectedAbuseEvents
from gatekeeper.models import AbuseEvent, RiskProfile

logger = logging.getLogger(__name__)


class PreflightService:
    
    def __init__(self, data: PreflightRequestData):
        self.data = data
        self.risk_profile = self._get_or_create_profile()
        self.abuse_detection_service = AbuseDetectionService(self.data)
        self.abuse_event_service = AbuseEventService(self.risk_profile, AbuseEventSourceEnum.PREFLIGHT)
        
    def _get_or_create_profile(self) -> RiskProfile:
        return RiskProfile.objects.get_or_create_by_phone(self.data.phone_number)[0]

    def detect_abuse_events(self) -> DetectedAbuseEvents:
        abuse_events = self.abuse_detection_service.run_checks()
        return abuse_events
    
    def record_abuse_events(self, abuse_events: DetectedAbuseEvents) -> list[AbuseEvent]:
        return self.abuse_event_service.record_events(abuse_events)
        