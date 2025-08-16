from street_ninja_common.cache import BaseRedisClient
from .access_patterns import GateAccessPattern
from .dataclasses import GateActivityData, UnixTimestamp
from .enums import GateCachePrefix
from django.utils import timezone
from typing import Any, Type


class GateActivityCacheClient(BaseRedisClient):
    
    def __init__(self, access_pattern: Type[GateAccessPattern]):
        super().__init__(access_pattern)
    
    def _activity_key(self, phone_number: str) -> str:
        return GateCachePrefix.activity_key(phone_number)
    
    
    def set(self, cache_data: GateActivityData):
        ...
    
    def get(self, phone_number: str) -> GateActivityData:
        cached_data: dict[str, Any] | None = self._get_cached_data(redis_key=self._activity_key(phone_number))
        if cached_data:
            return GateActivityData(
                valid_msgs = cached_data["valid_msgs"],
                invalid_msgs = cached_data["invalid_msgs"],
                last_updated = cached_data["last_updated"]
            )
        else:
            return GateActivityData(
                valid_msgs = [],
                invalid_msgs = [],
                last_updated = UnixTimestamp(timezone.now().timestamp()),
            )