import logging
from typing import Callable
from gatekeeper.enums import AbuseEventTypeEnum
from ..abuse_checks import AbuseChecks
from ..dataclasses import DetectedAbuseEvent, DetectedAbuseEvents
from ..exc import AbuseDetectionError
from ..schemas import PreflightRequestData


logger = logging.getLogger(__name__)


class ScreeningService:
    
    ABUSE_CHECK_TO_ABUSE_TYPE = {
        AbuseChecks.code_injection: AbuseEventTypeEnum.MALICIOUS,
        AbuseChecks.commercial_spam: AbuseEventTypeEnum.COMMERCIAL_SPAM,
        AbuseChecks.international_number: AbuseEventTypeEnum.INTERNATIONAL_NUMBER,
        AbuseChecks.sqli: AbuseEventTypeEnum.MALICIOUS,
        AbuseChecks.usa_number: AbuseEventTypeEnum.USA_NUMBER,
        AbuseChecks.voip_number: AbuseEventTypeEnum.VOIP_NUMBER,
    }

    def __init__(self, data: PreflightRequestData):
        self.data = data

    def run_checks(self) -> DetectedAbuseEvents:
        try:
            abuse_events = self._detect_abuse_events()
        except Exception as e:
            msg = f"{self.__class__.__name__} encountered an unexpected error while running abuse detection checks: {e}"
            logger.error(msg, exc_info=True)
            raise AbuseDetectionError(msg) from e
        else:
            logger.debug(f"{self.__class__.__name__} ran all abuse checks. Abuse events: `{abuse_events}`")
            return DetectedAbuseEvents(
                events=abuse_events,
                sms_id=self.data.sms_id,
                msg=self.data.msg,
            )

    def _detect_abuse_events(self) -> list[DetectedAbuseEvent]:
        abuse_events: list[DetectedAbuseEvent] = []
        for check, abuse_event_type_enum in self.ABUSE_CHECK_TO_ABUSE_TYPE.items():
            abuse_event = self._run_check(check, abuse_event_type_enum)
            if abuse_event:
                abuse_events.append(abuse_event)
        return abuse_events

    def _run_check(self, check: Callable, abuse_event_type_enum: AbuseEventTypeEnum) -> DetectedAbuseEvent | None:
        success = check(self.data)
        if not success:
            return DetectedAbuseEvent(
                method_name=check.__name__,
                abuse_event_type=abuse_event_type_enum,
            )
        

