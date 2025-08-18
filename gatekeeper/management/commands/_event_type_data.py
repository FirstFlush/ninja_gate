from ...enums import AbuseCategoryEnum, AbuseEventTypeEnum

EVENT_TYPE_DATA = [
   {
       "name": AbuseEventTypeEnum.INTERNATIONAL_NUMBER,
       "category": AbuseCategoryEnum.SYSTEM,
       "description": "Phone number from outside US/Canada",
   },
   {
       "name": AbuseEventTypeEnum.INVALID_AREA_CODE,
       "category": AbuseCategoryEnum.SYSTEM,
       "description": "Invalid or unrecognized area code",
   },
   {
       "name": AbuseEventTypeEnum.INVALID_NUMBER_TYPE,
       "category": AbuseCategoryEnum.SYSTEM,
       "description": "VoIP or commercial number (not mobile/landline)",
   },
   {
       "name": AbuseEventTypeEnum.MALICIOUS,
       "category": AbuseCategoryEnum.SECURITY,
       "description": "Message contains injection attempts or malicious patterns",
   },
   {
       "name": AbuseEventTypeEnum.COMMERCIAL_SPAM,
       "category": AbuseCategoryEnum.SECURITY,
       "description": "Spam, phishing, or unwanted commercial content",
   },
   {
       "name": AbuseEventTypeEnum.UNRESOLVED_MSG,
       "category": AbuseCategoryEnum.BEHAVIORAL,
       "description": "Message system cannot process or understand",
   },
   {
       "name": AbuseEventTypeEnum.INVALID_MSG_LENGTH,
       "category": AbuseCategoryEnum.SYSTEM,
       "description": "SMS message is too long, or too short. Check settings.py for max/min values",
   },
   {
       "name": AbuseEventTypeEnum.RESTRICTED_USER_ATTEMPT,
       "category": AbuseCategoryEnum.BEHAVIORAL,
       "description": "A currently banned or suspended user has sent a request to the service",
   },
]