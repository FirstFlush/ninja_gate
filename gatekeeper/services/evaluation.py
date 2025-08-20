from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from django.conf import settings
from gatekeeper.dataclasses import EvaluationData, PreflightEvaluationData, RiskProfileActionData
from gatekeeper.enums import RiskProfileStatus
from gatekeeper.models import AbuseEvent, AbuseEventTypeEnum, RiskProfileActionSource
from gatekeeper.preflight.dataclasses import PreflightEvaluation
from gatekeeper.preflight.enums import RequestAction

logger = logging.getLogger(__name__)


class EvaluationServiceError(Exception):
    """Raised when the EvaluationService fails for unknown reasons"""
    pass

class BaseRiskEvaluationService(ABC):

    FLAGGED_HOURS_DEFAULT = settings.FLAGGED_HOURS_DEFAULT
    SUSPENDED_DAYS_DEFAULT = settings.SUSPENDED_DAYS_DEFAULT
    
    ABUSE_EVENTS_MAX: int = settings.ABUSE_EVENTS_MAX
    ABUSE_TYPE_ACTIONS = {
        AbuseEventTypeEnum.INVALID_MSG_LENGTH: RiskProfileStatus.FLAGGED,
        AbuseEventTypeEnum.UNRESOLVED_MSG: RiskProfileStatus.FLAGGED,
        AbuseEventTypeEnum.INVALID_NUMBER_TYPE: RiskProfileStatus.SUSPENDED,
        AbuseEventTypeEnum.COMMERCIAL_SPAM: RiskProfileStatus.SUSPENDED,
        AbuseEventTypeEnum.MALICIOUS: RiskProfileStatus.SUSPENDED,
        AbuseEventTypeEnum.INTERNATIONAL_NUMBER: RiskProfileStatus.BANNED,
        AbuseEventTypeEnum.INVALID_AREA_CODE: RiskProfileStatus.BANNED,
    }
    SEVERITY_RANK = {
        RiskProfileStatus.ACTIVE: 0,
        RiskProfileStatus.FLAGGED: 1,
        RiskProfileStatus.SUSPENDED: 2, 
        RiskProfileStatus.BANNED: 3
    }

    def __init__(self, data: EvaluationData):
        self.data = data

    # @abstractmethod
    # def evaluate(self, **kwargs):
    #     pass

    def _is_within_threshold(self, threshold: int | None = None) -> bool:
        if threshold is None:
            threshold = self.ABUSE_EVENTS_MAX
        unique_msgs = set([event.sms_id for event in self.data.cached_data.abuse_events])
        return len(unique_msgs) < threshold

    def _db_action(self, event: AbuseEvent) -> RiskProfileActionData:
        match self.SEVERITY_RANK[self.ABUSE_TYPE_ACTIONS[event.event_type.enum]]:
            case 0:
                action = self._active(event)
            case 1:
                action = self._flagged(event)
            case 2:
                action = self._suspended(event)
            case 3:
                action = self._banned(event)
        return action

    def _create_action_data(
            self, 
            status: RiskProfileStatus, 
            event: AbuseEvent, 
            expiry: datetime | None = None, 
            notes: str | None = None
    ) -> RiskProfileActionData:
        
        return RiskProfileActionData(
            profile = self.data.profile,
            status = status,
            source = RiskProfileActionSource.PREFLIGHT,
            trigger_event = event,
            expiry = expiry,
            notes = notes,
        )

    def _active(self, event: AbuseEvent) -> RiskProfileActionData:
        return self._create_action_data(
            status=RiskProfileStatus.ACTIVE,
            event=event,
        )

    def _flagged(self, event: AbuseEvent) -> RiskProfileActionData:
        expiry = event.created + timedelta(hours=self.FLAGGED_HOURS_DEFAULT)
        if self._is_within_threshold():
            return self._active(event)
        else:
            return self._create_action_data(
                status=RiskProfileStatus.FLAGGED,
                event=event,
                expiry=expiry,
            )
    
    def _suspended(self, event: AbuseEvent) -> RiskProfileActionData:
        expiry = (event.created + timedelta(days=self.SUSPENDED_DAYS_DEFAULT)).replace(hour=0, minute=0, second=0, microsecond=0)
        return self._create_action_data(
            status=RiskProfileStatus.SUSPENDED,
            event=event,
            expiry=expiry
        )
    
    def _banned(self, event: AbuseEvent) -> RiskProfileActionData:
        return self._create_action_data(status=RiskProfileStatus.BANNED, event=event,)


class PreflightEvaluationService(BaseRiskEvaluationService):

    REQUEST_ACTIONS = {
        RiskProfileStatus.ACTIVE: RequestAction.PROCEED,
        RiskProfileStatus.FLAGGED: RequestAction.PROCEED_DROP_JUNK,
        RiskProfileStatus.SUSPENDED: RequestAction.DROP,
        RiskProfileStatus.BANNED: RequestAction.DROP,
    }

    def __init__(self, data: PreflightEvaluationData):
        self.data = data

    def _most_severe_abuse_event(self) -> AbuseEvent:
        
        if not self.data.current_events:
            msg = f"{self.__class__.__name__} received invalid data.current_events: {self.data.current_events}"
            logger.error(msg)
            raise RuntimeError(msg)

        return max(
            self.data.current_events, 
            key=lambda event: self.SEVERITY_RANK[self.ABUSE_TYPE_ACTIONS[event.event_type.enum]]
        )
    
    def _request_action(self, status: RiskProfileStatus) -> RequestAction:
        return self.REQUEST_ACTIONS[status]
    
    def evaluate(self) -> PreflightEvaluation:
        event = self._most_severe_abuse_event()
        db_action = self._db_action(event)
        return PreflightEvaluation(
            db_action = db_action,
            request_action = self._request_action(db_action.status)
        )

class PostflightEvaluationService(BaseRiskEvaluationService):


    def evaluate(self):
        ...