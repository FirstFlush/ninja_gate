from common.base_enum import StreetNinjaEnum


class RiskLevelEnum(StreetNinjaEnum):

    LOW = "low"                     # 0-30: Clean/active
    MODERATE = "moderate"           # 31-60: Flagged/monitored
    HIGH = "high"                   # 61-90: Rate limited/soft blocked
    BLOCKED = "blocked"             # 91-100: Hard blocked/banned


class RiskProfileStatus(StreetNinjaEnum):
   ACTIVE = "active"                # Normal service, no restrictions
   FLAGGED = "flagged"              # Elevated monitoring, won't receive help message again for jibberish replies
   RATE_LIMITED = "rate_limited"    # Throttled messaging (e.g., max 3 messages/hour)
   SUSPENDED = "suspended"          # Temporary timeout (6-24 hours), auto-expires
   BANNED = "banned"                # Permanent restriction, admin override only


class AbuseCategoryEnum(StreetNinjaEnum):
    
    SECURITY = "security"
    BEHAVIORAL = "behavioral"
    SYSTEM = "system"


class AbuseEventTypeEnum(StreetNinjaEnum):

    MALICIOUS = "malicious"
    INTERNATIONAL_NUMBER = "international_number"
    USA_NUMBER = "usa_number"       # international number, but with country code 1.
    VOIP_NUMBER = "voip_number"
    FRUSTRATED_USER = "frustrated_user"
    COMMERCIAL_SPAM = "commercial_spam"
    
    
class AbuseEventSourceEnum(StreetNinjaEnum):
    
    PREFLIGHT = "preflight"
    POST_ANALYSIS = "post_analysis"
    
