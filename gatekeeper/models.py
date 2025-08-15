from django.db import models, IntegrityError, DatabaseError
from django.utils import timezone
import logging
from .enums import (
    AbuseEventTypeEnum, 
    AbuseCategoryEnum, 
    AbuseEventSourceEnum,
    RiskProfileStatus,
    RiskLevelEnum
)


logger = logging.getLogger(__name__)


class RiskProfileManager(models.Manager):
      
    def get_or_create_by_phone(self, phone_number: str) -> tuple["RiskProfile", bool]:
        try:
            profile, created = RiskProfile.objects.get_or_create(
                phone_number=phone_number,
                defaults={
                    "last_seen": timezone.now(),
                }
            )
            
        except IntegrityError as e:
            msg = f"Could not get or create RiskProfile due to integrity error!"
            logger.error(msg, exc_info=True)
            raise
        
        except DatabaseError as e:
            msg = f"Could not get or create RiskProfile due to unexpected database error `{e.__class__.__name__}`"
            logger.error(msg, exc_info=True)
            raise
        
        else:
            logger.debug(f"RiskProfile for phone number: `{profile.phone_number}`, created: `{created}`")
            return profile, created


class RiskProfile(models.Model):
    
    phone_number = models.CharField(max_length=20, unique=True)
    risk_level = models.CharField(max_length=24, choices=RiskLevelEnum.choices, default=RiskLevelEnum.LOW.value)
    status = models.CharField(max_length=24, choices=RiskProfileStatus.choices, default=RiskProfileStatus.ACTIVE.value)
    last_seen = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    objects: RiskProfileManager = RiskProfileManager()

class AbuseEventType(models.Model):
    name = models.CharField(max_length=24, choices=AbuseEventTypeEnum.choices, unique=True)
    category = models.CharField(max_length=24, choices=AbuseCategoryEnum.choices)
    description = models.TextField(null=True, blank=True)   # Optional: human-readable description
    risk_level = models.CharField(max_length=24, choices=RiskLevelEnum.choices)


class AbuseEvent(models.Model):
    profile = models.ForeignKey(to=RiskProfile, on_delete=models.CASCADE)
    event_type = models.ForeignKey(to=AbuseEventType, on_delete=models.CASCADE)
    source = models.CharField(max_length=24, choices=AbuseEventSourceEnum.choices)
    message_content = models.TextField(null=True, blank=True)
    sms_id = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)