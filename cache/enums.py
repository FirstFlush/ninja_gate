from street_ninja_common.cache import RedisKeyEnum


class GateCachePrefix(RedisKeyEnum):

    ACTIVITY = "gate:activity:"
    
    @classmethod
    def activity_key(cls, phone_number: str) -> str:
        return f"{cls.ACTIVITY.value}{phone_number}"