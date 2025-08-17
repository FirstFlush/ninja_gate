from street_ninja_common.cache import CacheClient, CacheCircuitBreaker
from .access_patterns import GateActivityAccessPattern
from .dataclasses import GateActivityData
from django.utils import timezone


class GateActivityCacheService:

    def __init__(self):
        self.circuit_breaker = CacheCircuitBreaker()
        self.access_pattern = GateActivityAccessPattern()
        self.client = CacheClient[GateActivityData](self.circuit_breaker)

    def set_activity(self, phone_number: str, data: GateActivityData | None = None):
        if data is None:
            data = self._create_activity()
        else:
            data.last_updated = timezone.now().timestamp()
        self.client.set(value=data, access_pattern=self.access_pattern, phone_number=phone_number)

    def _create_activity(self) -> GateActivityData:
        return GateActivityData(
            valid_msgs = [],
            invalid_msgs = [],
            last_updated = timezone.now().timestamp(),
        )

    def get_activity(self, phone_number: str) -> GateActivityData:
        cached_data = self.client.get(self.access_pattern, phone_number=phone_number)
        if cached_data:
            return cached_data
        else:
            return self._create_activity()