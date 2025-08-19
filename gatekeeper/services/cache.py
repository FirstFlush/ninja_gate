import bisect
from django.conf import settings
from django.db.models import QuerySet
from django.utils import timezone
from street_ninja_common.cache import CacheClient, CacheCircuitBreaker
from ..models import AbuseEvent
from cache.access_patterns import GateActivityAccessPattern
from cache.dataclasses import GateActivityData, AbuseEventCache


class GateActivityCacheService:

    ABUSE_EVENTS_WINDOW = settings.ABUSE_EVENTS_WINDOW
    
    def __init__(self):
        self.circuit_breaker = CacheCircuitBreaker()
        self.access_pattern = GateActivityAccessPattern()
        self.client = CacheClient[GateActivityData](self.circuit_breaker)

    def get_cache(self, phone_number: str) -> GateActivityData:
        cached_data = self.client.get(self.access_pattern, phone_number=phone_number)
        if cached_data:
            return self._hydrate_cache_data(cached_data) 
        else:
            return self._create_cache()

    def update_cache(
            self, 
            phone_number: str, 
            abuse_events: QuerySet[AbuseEvent],
            last_updated: float | None = None
    ) -> GateActivityData:
        if last_updated is None:
            last_updated = self._timestamp()
        abuse_events_cache = [abuse_event.to_cache() for abuse_event in abuse_events]
        activity_data = self.get_cache(phone_number)
        activity_data.abuse_events.extend(abuse_events_cache)
        activity_data.last_updated = last_updated
        self.set_cache(phone_number, activity_data)
        return activity_data

    def reset_cache(self, phone_number: str):
        self.set_cache(phone_number, data=self._create_cache())

    def set_cache(self, phone_number: str, data: GateActivityData | None = None):
        if data is None:
            data = self._create_cache()
        else:
            data.last_updated = self._timestamp()
        data.abuse_events.sort(key=lambda x: x.timestamp)
        self._truncate_by_timestamp(data)
        self.client.set(value=data, access_pattern=self.access_pattern, phone_number=phone_number)

    @staticmethod
    def _timestamp() -> float:
        return timezone.now().timestamp()
    
    def _hydrate_cache_data(self, cached_data: GateActivityData) -> GateActivityData:
        """Convert list of dicts back to AbuseEventCache objects"""
        if cached_data.abuse_events:
            cached_data.abuse_events = [
                AbuseEventCache(**event_dict) if isinstance(event_dict, dict) else event_dict
                for event_dict in cached_data.abuse_events
            ]
        return cached_data

    def _truncate_by_timestamp(self, data: GateActivityData):
        target = data.last_updated - self.ABUSE_EVENTS_WINDOW
        i = bisect.bisect_left(data.abuse_events, target, key=lambda x: x.timestamp)
        data.abuse_events = data.abuse_events[i:]
        
    def _create_cache(self, last_updated: int | None = None) -> GateActivityData:
        return GateActivityData(
            abuse_events = [],
            last_updated = last_updated if last_updated is not None else self._timestamp(),
        )