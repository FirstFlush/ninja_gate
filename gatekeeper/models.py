from django.db import models


class PhoneNumberRiskProfile(models.Model):
    
    phone_number = models.CharField(max_length=20, unique=True)
    
    last_seen = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)



class AbuseEvent(models.Model):
    
    profile = models.ForeignKey(to=PhoneNumberRiskProfile, on_delete=models.CASCADE, related_name="abuse_events")
