import logging
from django.db import transaction
from ..enums import RiskProfileStatus
from ..dataclasses import StatusChangeData
from ..models import RiskProfile, RiskProfileStatusChange


logger = logging.getLogger(__name__)


class RiskStatusService:
    
    def __init__(self, status_change: StatusChangeData):
        self.data = status_change
        self.prev_status = self.data.profile.status
    
    def change_status(self):
        with transaction.atomic():
            self._update_risk_profile()
            self._create_status_change()
        
    @staticmethod
    def expire_status(risk_profile: RiskProfile):
        risk_profile.status = RiskProfileStatus.ACTIVE.value
        risk_profile.save()
        logger.debug(f"RiskProfile for phone number `{risk_profile.phone_number}` status lowered to ACTIVE")
        
        
    def _create_status_change(self):
        
        RiskProfileStatusChange.objects.create(
            profile = self.data.profile,
            prev_status = self.prev_status,
            trigger_event = self.data.trigger_event,
            new_status = self.data.new_status,
            effective_at = self.data.effective_at,
            expires_at = self.data.expires_at,
            notes = self.data.notes,
        )
        
    def _update_risk_profile(self):
        self.data.profile.change_status(self.data.new_status)