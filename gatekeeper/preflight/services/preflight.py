import logging
from django.db.models import QuerySet
from gatekeeper.enums import AbuseEventSourceEnum
from ..schemas import PreflightRequestData
from .screening import ScreeningService
from ..dataclasses import DetectedAbuseEvents, PreflightEvaluation
from cache.dataclasses import GateActivityData
from gatekeeper.dataclasses import PreflightEvaluationData
from gatekeeper.models import AbuseEvent, RiskProfile
from gatekeeper.services.cache import GateActivityCacheService
from gatekeeper.services.evaluation import PreflightEvaluationService, EvaluationServiceError
from gatekeeper.services.recording import AbuseRecordingService
from gatekeeper.services.risk_profile_action import RiskProfileActionService

logger = logging.getLogger(__name__)


class PreflightService:
    
    def __init__(self, data: PreflightRequestData):
        self.data = data
        self.risk_profile = self._get_or_create_profile()
        self.screening_service = ScreeningService(data=self.data, profile=self.risk_profile)
        self.recording_service = AbuseRecordingService(self.risk_profile, AbuseEventSourceEnum.PREFLIGHT)
        self.cache_service = GateActivityCacheService()
        self._evaluation_cls = PreflightEvaluationService
        self._profile_action_cls = RiskProfileActionService

    def main(self):
        abuse_events = self._screen_for_abuse()
        if abuse_events:
            abuse_event_records = self._record_abuse_events(abuse_events)
            cached_data = self._update_cache(abuse_event_records)
            evaluation_data = self._evaluation_data(cached_data, abuse_event_records)
            self._evaluate(evaluation_data)
            # risk profile action service
            # build response


    def _evaluation_data(
            self, 
            cached_data: GateActivityData,
            abuse_events: QuerySet[AbuseEvent],
    ) -> PreflightEvaluationData:
        return PreflightEvaluationData(
            profile=self.risk_profile,
            cached_data=cached_data,
            current_events=abuse_events,
            msg=self.data.msg,
        )

    def _evaluate(self, data: PreflightEvaluationData) -> PreflightEvaluation:
        try:
            service = self._evaluation_cls(data)
        except Exception as e:
            msg = f"Failed to instantiate PreflightEvaluationService due to an unknown error: {e}"
            logger.error(msg, exc_info=True)
            raise EvaluationServiceError from e
        else:
            try:
                evaluation_data = service.evaluate()
            except Exception as e:
                msg = f"Failed to build PreflightEvaluation due to an unknown error: {e}"
                logger.error(msg, exc_info=True)
                raise EvaluationServiceError from e
            else:
                logger.debug(f"Successfull created {evaluation_data.__class__.__name__}")
                return evaluation_data

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