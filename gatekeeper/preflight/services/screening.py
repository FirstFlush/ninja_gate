import logging
import phonenumbers
from typing import Callable
from gatekeeper.enums import AbuseEventTypeEnum
from ..screening_checks import ScreeningChecks
from ..dataclasses import DetectedAbuseEvent, DetectedAbuseEvents, ScreeningCheckData
from ..exc import AbuseDetectionError
from ..schemas import PreflightRequestData


logger = logging.getLogger(__name__)


class ScreeningService:
    
    ABUSE_CHECK_TO_ABUSE_TYPE = {
        ScreeningChecks.country_code: AbuseEventTypeEnum.INTERNATIONAL_NUMBER,
        ScreeningChecks.area_code: AbuseEventTypeEnum.INVALID_AREA_CODE,
        ScreeningChecks.voip_number: AbuseEventTypeEnum.VOIP_NUMBER,
        ScreeningChecks.appropriate_length: AbuseEventTypeEnum.INVALID_MSG_LENGTH,
        # ScreeningChecks.code_injection: AbuseEventTypeEnum.MALICIOUS,
        # ScreeningChecks.commercial_spam: AbuseEventTypeEnum.COMMERCIAL_SPAM,
        # ScreeningChecks.sqli: AbuseEventTypeEnum.MALICIOUS,
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

    def _screening_data(self) -> ScreeningCheckData:
        return ScreeningCheckData(
            phone_number=self.data.phone_number,
            msg=self.data.msg,
            parsed_number=phonenumbers.parse(self.data.phone_number),
        )

    def _run_check(self, check: Callable, abuse_event_type_enum: AbuseEventTypeEnum) -> DetectedAbuseEvent | None:
        screening_data = self._screening_data()
        success: bool = check(screening_data)
        if not success:
            logger.debug(f"Preflight check FAILED: `{check.__name__}`")
            return DetectedAbuseEvent(
                abuse_event_type=abuse_event_type_enum,
                context={"Preflight check": check.__name__},
            )
        

