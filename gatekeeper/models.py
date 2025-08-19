from datetime import datetime
from django.db import models, IntegrityError, DatabaseError
from django.utils import timezone
import logging
from .enums import (
    AbuseEventTypeEnum, 
    AbuseCategoryEnum, 
    AbuseEventSourceEnum,
    RiskProfileStatus,
)
from cache.dataclasses import AbuseEventCache


logger = logging.getLogger(__name__)


class RiskProfileManager(models.Manager):

    def get_or_create_by_phone(self, phone_number: str) -> tuple["RiskProfile", bool]:
        try:
            query_result: tuple["RiskProfile", bool] = self.get_or_create(
                phone_number=phone_number,
                defaults={
                    "last_seen": timezone.now(),
                }
            )
            profile, created = query_result
        except IntegrityError as e:
            msg = f"Could not get or create RiskProfile due to an IntegirtyError for phone number `{phone_number}`"
            logger.error(msg, exc_info=True)
            raise
        
        except DatabaseError as e:
            msg = f"Could not get or create RiskProfile due to database error `{e.__class__.__name__}` for phone number `{phone_number}`"
            logger.error(msg, exc_info=True)
            raise

        except Exception as e:
            msg = f"Could not get or create RiskProfile due to an unexpected error `{e.__class__.__name__}` for phone number `{phone_number}`"
            logger.error(msg, exc_info=True)
            raise

        else:
            logger.debug(f"RiskProfile for phone number: `{profile.phone_number}`, created: `{created}`")
            return profile, created


class RiskProfile(models.Model):
    
    phone_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=24, choices=RiskProfileStatus.choices, default=RiskProfileStatus.ACTIVE.value)
    last_seen = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    objects: RiskProfileManager = RiskProfileManager()

    def __str__(self) -> str:
        return self.phone_number
    
    def change_status(self, new_status: RiskProfileStatus):
        old_status = self.status
        self.status = new_status.value
        self.save()    
        logger.debug(f"Changed RiskProfile `{self.__str__()}` status from {old_status} to {new_status.value}")


class AbuseEventType(models.Model):
    name = models.CharField(max_length=24, choices=AbuseEventTypeEnum.choices, unique=True)
    category = models.CharField(max_length=24, choices=AbuseCategoryEnum.choices)
    description = models.TextField(null=True, blank=True)   # Optional: human-readable description

    def __str__(self) -> str:
        return self.name


class AbuseEvent(models.Model):
    profile = models.ForeignKey(to=RiskProfile, on_delete=models.CASCADE, related_name="events")
    event_type = models.ForeignKey(to=AbuseEventType, on_delete=models.CASCADE, related_name="events")
    source = models.CharField(max_length=24, choices=AbuseEventSourceEnum.choices)
    sms_id = models.IntegerField()
    context = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.profile.phone_number} | {self.event_type}"

    def to_cache(self, dt: datetime | None = None) -> AbuseEventCache:
        timestamp = timezone.now().timestamp() if dt is None else dt.timestamp()
        return AbuseEventCache(
            abuse_type=self.event_type.name,
            timestamp=timestamp,
        )


class RiskProfileStatusChange(models.Model):
    
    profile = models.ForeignKey(to=RiskProfile, on_delete=models.CASCADE, related_name='status_changes')
    prev_status = models.CharField(max_length=24, choices=RiskProfileStatus.choices)
    new_status = models.CharField(max_length=24, choices=RiskProfileStatus.choices)
    effective_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    trigger_event = models.ForeignKey(to=AbuseEvent, on_delete=models.SET_NULL, null=True, blank=True)
    # created_by = models.CharField(max_length=50, default='system')  # 'system', 'admin', 'auto_expire'
    
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['profile', 'expires_at']),
            models.Index(fields=['expires_at']),
        ]