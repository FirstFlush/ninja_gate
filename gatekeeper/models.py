from django.db import models
from .enums import (
    AbuseEventTypeEnum, 
    AbuseCategoryEnum, 
    AbuseEventSourceEnum,
    RiskProfileStatus,
    RiskLevelEnum
)

class RiskProfile(models.Model):
    
    phone_number = models.CharField(max_length=20, unique=True)
    risk_level = models.CharField(max_length=24, choices=RiskLevelEnum.choices, default=RiskLevelEnum.LOW.value)
    status = models.CharField(max_length=24, choices=RiskProfileStatus.choices, default=RiskProfileStatus.ACTIVE.value)
    last_seen = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)


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