from dataclasses import dataclass
from typing import Any, Type
from .dataclasses import GateActivityData
from street_ninja_common.cache import Seconds, CacheKey, BaseCacheAccessPattern, CacheStoreEnum

from .enums import NinjaGateCacheKey


@dataclass(frozen=True)
class GateActivityAccessPattern(BaseCacheAccessPattern):
    store: CacheStoreEnum = CacheStoreEnum.GATE
    _key_enum: CacheKey = NinjaGateCacheKey.GATE_ACTIVITY
    ttl: Seconds = Seconds.DAY
    value_type: Type[Any] = GateActivityData

    def key(self, phone_number: str) -> str:
        return f"{self._key_enum.value}{phone_number}"