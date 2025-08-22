import logging
from gatekeeper.dataclasses import GateActivityData
from gatekeeper.enums import AbuseEventSourceEnum
from gatekeeper.models import RiskProfile
from gatekeeper.services import RiskProfileActionService, GateActivityCacheService, AbuseRecordingService
from .response import PostflightResponseService
from ..schemas import PostflightRequestData


logger = logging.getLogger(__name__)


class PostflightService:
    
    def __init__(self, data: PostflightRequestData):
        self.data = data
        self.risk_profile = self._get_or_create_profile()
        self.recording_service = AbuseRecordingService(self.risk_profile, AbuseEventSourceEnum.POSTFLIGHT)

        self.cache_service = GateActivityCacheService()
        self._profile_action_cls = RiskProfileActionService
        self._response_cls = PostflightResponseService
    
    def _get_cached_data(self) -> GateActivityData:
        data =  self.cache_service.get_cache(phone_number=self.data.phone_number)
        logger.debug(f"Retrieved cached data: {data}")
        return data
    
    def _get_or_create_profile(self) -> RiskProfile:
        profile, created = RiskProfile.objects.get_or_create_by_phone(self.data.phone_number)
        if created:
            logger.warning(f"RiskProfile for phone number `{self.data.phone_number}` was CREATED during postflight!")
        return profile