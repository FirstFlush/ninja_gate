from django.db import DatabaseError
import logging
from ..preflight.dataclasses import DetectedAbuseEvent, DetectedAbuseEvents
from ..preflight.exc import AbuseEventServiceError
from gatekeeper.models import AbuseEvent, RiskProfile, AbuseEventType
from gatekeeper.enums import AbuseEventSourceEnum


logger = logging.getLogger(__name__)

class AbuseRecordingService:
    
    def __init__(self, risk_profile: RiskProfile, source: AbuseEventSourceEnum):
        self.risk_profile = risk_profile
        self.source = source

    
    def record_events(self, abuse_events: DetectedAbuseEvents) -> list[AbuseEvent]:
        try:
            event_type_mapping = self._build_event_type_mapping(abuse_events.events)
        except Exception as e:
            msg = f"{self.__class__.__name__} received unexpected error `{e.__class__.__name__}` while building event_type_mapping"
            logger.error(msg, exc_info=True)
            raise AbuseEventServiceError(msg) from e
        
        try:
            saved_events = self._save_abuse_events(abuse_events, event_type_mapping)
        except DatabaseError as e:
            msg = f"Unexpected `{e.__class__.__name__}` while attempting to save `{len(abuse_events.events)}` AbuseEvent records for phone# `{self.risk_profile.phone_number}` and sms_id `{abuse_events.sms_id}`"
            logger.error(msg, exc_info=True)
            raise AbuseEventServiceError(msg) from e
        else:
            logger.debug(f"Saved `{len(saved_events)}` AbuseEvent records for phone# `{self.risk_profile.phone_number}`")
            return saved_events

    def _build_event_type_mapping(self, abuse_events: list[DetectedAbuseEvent]) -> dict[str, AbuseEventType]:
        """
        Build a mapping from event type names to AbuseEventType objects.
        
        Takes a list of detected abuse events, extracts the unique event type names,
        queries the database for the corresponding AbuseEventType objects, and returns
        a dictionary mapping each name to its database object.
        """
        event_type_names = {event.abuse_event_type.value for event in abuse_events}
        qs = AbuseEventType.objects.filter(name__in=event_type_names)
        return {event_type.name: event_type for event_type in qs}
    
    def _save_abuse_events(
            self, 
            abuse_events: DetectedAbuseEvents,
            event_type_mapping: dict[str, AbuseEventType],
    ) -> list[AbuseEvent]:
        
        to_save = [AbuseEvent(
            profile = self.risk_profile,
            event_type = event_type_mapping[abuse_event.abuse_event_type.value],
            source = self.source.value,
            context = abuse_event.context,
            sms_id = abuse_events.sms_id,
        ) for abuse_event in abuse_events.events]

        return AbuseEvent.objects.bulk_create(to_save)
        