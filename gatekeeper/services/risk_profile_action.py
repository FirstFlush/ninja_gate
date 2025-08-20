from datetime import datetime
import logging
from django.db import transaction
from django.utils import timezone
from ..enums import RiskProfileStatus, RiskProfileActionSource
from ..dataclasses import RiskProfileActionData
from ..models import RiskProfile, RiskProfileAction


logger = logging.getLogger(__name__)


class RiskProfileActionService:

    def __init__(self, action_data: RiskProfileActionData):
        self.data = action_data
        self.prev_status = self.data.profile.status

    @classmethod
    def change_status(cls, status_change: RiskProfileActionData) -> RiskProfileAction:
        service = cls(status_change)
        return service._change_status()

    @classmethod
    def expire_status(
            cls, 
            risk_profile: RiskProfile,
            source: RiskProfileActionSource,
            notes: str = "Automatic expiration",
            effective_at: datetime | None = None,
    ) -> RiskProfileAction:
        
        if effective_at is None:
            effective_at = timezone.now()
            
        data = RiskProfileActionData(
            profile=risk_profile,
            status=RiskProfileStatus.ACTIVE,
            source=source,
            notes=notes,
        )
        
        service = cls(data)
        return service._change_status()        

    def _change_status(self) -> RiskProfileAction:
        try:
            with transaction.atomic():
                self._update_risk_profile()
                status_change_object = self._create_status_change()
        except Exception:
            msg = f"Failed to change status for phone number `{self.data.profile.phone_number}` from `{self.prev_status}` to `{self.data.status.value}`"
            logger.error(msg, exc_info=True)
            raise 
        else:
            logger.debug(f"Successfully changed status for phone number `{self.data.profile.phone_number}` from `{self.prev_status}` to `{self.data.status.value}`")
            return status_change_object

    def _create_status_change(self) -> RiskProfileAction:
        return RiskProfileAction.objects.create(
            profile = self.data.profile,
            prev_status = self.prev_status,
            trigger_event = self.data.trigger_event,
            new_status = self.data.status,
            notes = self.data.notes,
            source=self.data.source,
        )

    def _update_risk_profile(self):
        self.data.profile.change_status(self.data.status, self.data.expiry)
        