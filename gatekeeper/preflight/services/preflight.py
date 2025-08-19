import logging
from django.db.models import QuerySet
from gatekeeper.enums import AbuseEventSourceEnum
from ..schemas import PreflightRequestData
from .screening import ScreeningService
from ..dataclasses import DetectedAbuseEvents, PreflightEvaluationData
from cache.dataclasses import GateActivityData
from gatekeeper.models import AbuseEvent, RiskProfile
from gatekeeper.services.cache import GateActivityCacheService
from gatekeeper.services.evaluation import PreflightEvaluationService
from gatekeeper.services.recording import AbuseRecordingService
from gatekeeper.services.risk_status import RiskStatusService

logger = logging.getLogger(__name__)


class PreflightService:
    
    def __init__(self, data: PreflightRequestData):
        self.data = data
        self.risk_profile = self._get_or_create_profile()
        self.screening_service = ScreeningService(data=self.data, profile=self.risk_profile)
        self.recording_service = AbuseRecordingService(self.risk_profile, AbuseEventSourceEnum.PREFLIGHT)
        self.cache_service = GateActivityCacheService()
        self._evaluation_cls = PreflightEvaluationService
        self._risk_status_cls = RiskStatusService

    def main(self):
        abuse_events = self._screen_for_abuse()
        if abuse_events:
            abuse_event_records = self._record_abuse_events(abuse_events)
            cached_data = self._update_cache(abuse_event_records)
            evaluation_data = self._evaluation_data(abuse_event_records, cached_data)
            self._evaluate(evaluation_data)

    def _evaluation_data(
            self, 
            abuse_events: QuerySet[AbuseEvent], 
            cached_data: GateActivityData
    ) -> PreflightEvaluationData:
        return PreflightEvaluationData(
            profile=self.risk_profile,
            cached_data=cached_data,
            abuse_events=abuse_events,
        )

    def _evaluate(self, data: PreflightEvaluationData): 
        PreflightEvaluationService(data)

    def _update_cache(self, events: QuerySet[AbuseEvent]) -> GateActivityData:
        return self.cache_service.update_cache(
            phone_number=self.data.phone_number,
            abuse_events=events,
        )

    def _screen_for_abuse(self) -> DetectedAbuseEvents | None:
        abuse_events = self.screening_service.run_checks()
        if len(abuse_events.events) > 0:
            return abuse_events
        return None
    
    def _record_abuse_events(self, abuse_events: DetectedAbuseEvents) -> QuerySet[AbuseEvent]:
        return self.recording_service.record_events(abuse_events)
           
    def _get_or_create_profile(self) -> RiskProfile:
        return RiskProfile.objects.get_or_create_by_phone(self.data.phone_number)[0]