from common.base_enum import StreetNinjaEnum


class RiskProfileStatus(StreetNinjaEnum):
    """
    Risk assessment levels for phone numbers interacting with the SMS service.
    
    This enum defines escalating restriction levels based on usage patterns and 
    geographic/technical factors. Designed for cost optimization and fraud prevention
    in a Canadian homeless services SMS system.
    
    Levels (in order of restriction):
    
    ACTIVE: Normal service with full functionality. Phone number has no identified
            issues and receives standard service including help messages for 
            unrecognized input.
    
    FLAGGED: Cost optimization mode. Phone number can still use the service normally
                for legitimate requests, but will not receive help messages when sending
                gibberish/unrecognized input to avoid SMS costs. Typically auto-expires
                after 6-24 hours.
    
    SUSPENDED: Temporary complete service block. Applied to numbers that may be
                legitimately recycled to new users (VoIP numbers, numbers sending
                malicious content). Prevents all service interaction for 1-3 months
                to allow number recycling. Auto-expires.
    
    BANNED: Permanent service restriction. Applied to numbers that will never be
            valid for Canadian homeless services (international numbers, confirmed
            non-Canadian regions). Requires admin override to remove.
    """
    ACTIVE = "active"               # Normal service
    FLAGGED = "flagged"             # No help messages sent on gibberish, but can still use service
    SUSPENDED = "suspended"         # Complete block (VoIP, suspicious chars - temp recyclable numbers)  
    BANNED = "banned"               # Permanent block (international, confirmed invalid regions)


class AbuseCategoryEnum(StreetNinjaEnum):
    
    SECURITY = "security"
    BEHAVIORAL = "behavioral"
    SYSTEM = "system"


class AbuseEventTypeEnum(StreetNinjaEnum):

    MALICIOUS = "malicious"
    INVALID_MSG_LENGTH = "invalid_msg_length"
    INTERNATIONAL_NUMBER = "international_number"
    INVALID_AREA_CODE = "invalid_area_code"         # international number, but with country code 1.
    INVALID_NUMBER_TYPE = "invalid_number_type"     # VoIP or commercial numbers
    UNRESOLVED_MSG = "unresolved_msg"
    COMMERCIAL_SPAM = "commercial_spam"
    RESTRICTED_USER_ATTEMPT = "restricted_user_attempt"


class AbuseEventSourceEnum(StreetNinjaEnum):
    
    PREFLIGHT = "preflight"
    POST_ANALYSIS = "postflight"
    
class RiskProfileActionSource(StreetNinjaEnum):
    
    PREFLIGHT = "preflight"
    POST_ANALYSIS = "postflight"
    MANUAL = "manual"
    AUTO_EXPIRE = "auto_expire"