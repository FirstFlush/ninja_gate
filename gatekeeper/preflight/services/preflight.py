import logging
from gatekeeper.enums import AbuseEventSourceEnum
from ..schemas import PreflightRequestData
from .screening import ScreeningService
from .abuse_event import AbuseEventService
from ..dataclasses import DetectedAbuseEvents
from gatekeeper.models import AbuseEvent, RiskProfile

logger = logging.getLogger(__name__)


class PreflightService:
    
    def __init__(self, data: PreflightRequestData):
        self.data = data
        self.risk_profile = self._get_or_create_profile()
        self.screening_service = ScreeningService(self.data)
        self.abuse_event_service = AbuseEventService(self.risk_profile, AbuseEventSourceEnum.PREFLIGHT)
        
    def _get_or_create_profile(self) -> RiskProfile:
        return RiskProfile.objects.get_or_create_by_phone(self.data.phone_number)[0]

    def screen_for_abuse(self) -> DetectedAbuseEvents:
        abuse_events = self.screening_service.run_checks()
        return abuse_events
    
    def record_abuse_events(self, abuse_events: DetectedAbuseEvents) -> list[AbuseEvent]:
        return self.abuse_event_service.record_events(abuse_events)
        