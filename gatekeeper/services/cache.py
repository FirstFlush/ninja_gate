import bisect
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from street_ninja_common.cache import CacheClient, CacheCircuitBreaker
from cache.access_patterns import GateActivityAccessPattern
from cache.dataclasses import GateActivityData


class GateActivityCacheService:

    ABUSE_EVENTS_WINDOW = settings.ABUSE_EVENTS_WINDOW
    
    def __init__(self):
        self.circuit_breaker = CacheCircuitBreaker()
        self.access_pattern = GateActivityAccessPattern()
        self.client = CacheClient[GateActivityData](self.circuit_breaker)

    def get_cache(self, phone_number: str) -> GateActivityData:
        cached_data = self.client.get(self.access_pattern, phone_number=phone_number)
        if cached_data:
            return cached_data
        else:
            return self._create_activity()

    def update_cache(
            self, 
            phone_number: str, 
            timestamps: list[float], 
            last_updated: float | None = None
    ) -> GateActivityData:
        if last_updated is None:
            last_updated = self._timestamp()
        activity_data = self.get_cache(phone_number)
        activity_data.invalid_msgs.extend(timestamps)
        activity_data.last_updated = last_updated
        self.set_cache(phone_number, activity_data)
        return activity_data

    def reset_cache(self, phone_number: str):
        self.set_cache(phone_number, data=self._create_activity())

    def set_cache(self, phone_number: str, data: GateActivityData | None = None):
        if data is None:
            data = self._create_activity()
        else:
            data.last_updated = self._timestamp()
        data.invalid_msgs.sort()
        self._truncate_timestamps(data)
        self.client.set(value=data, access_pattern=self.access_pattern, phone_number=phone_number)

    @staticmethod
    def _timestamp() -> float:
        return timezone.now().timestamp()

    def _truncate_timestamps(self, data: GateActivityData):
        target = data.last_updated - self.ABUSE_EVENTS_WINDOW
        i = bisect.bisect_left(data.invalid_msgs, target)
        data.invalid_msgs = data.invalid_msgs[i:]
        
    def _create_activity(self, last_updated: int | None = None) -> GateActivityData:
        return GateActivityData(
            invalid_msgs = [],
            last_updated = last_updated if last_updated is not None else self._timestamp(),
        )

