from street_ninja_common.cache import BaseRedisAccessPattern
from street_ninja_common.cache import RedisStoreEnum, RedisKeyTTL
from .enums import GateCachePrefix


class GateAccessPattern(BaseRedisAccessPattern):

    redis_store_enum = RedisStoreEnum.GATE
    key_ttl_enum = RedisKeyTTL.DAY
    redis_key_enum =GateCachePrefix.ACTIVITY