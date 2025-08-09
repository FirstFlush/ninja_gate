from common.base_enum import StreetNinjaEnum


class RiskLevelEnum(StreetNinjaEnum):

    LOW = "low"                 # 0-30: Clean/active
    MODERATE = "moderate"       # 31-60: Flagged/monitored
    HIGH = "high"               # 61-90: Rate limited/soft blocked
    BLOCKED = "blocked"         # 91-100: Hard blocked/banned


class RiskProfileStatus(StreetNinjaEnum):
   ACTIVE = "active"              # Normal service, no restrictions
   FLAGGED = "flagged"            # Elevated monitoring, full service but watching for patterns
   RATE_LIMITED = "rate_limited"  # Throttled messaging (e.g., max 3 messages/hour)
   SOFT_BLOCKED = "soft_blocked"  # Temporary timeout (6-24 hours), auto-expires
   HARD_BLOCKED = "hard_blocked"  # Extended timeout (3-7 days), requires manual review to lift
   BANNED = "banned"              # Permanent restriction, admin override only


class AbuseCategoryEnum(StreetNinjaEnum):
    
    SECURITY = "security"
    BEHAVIORAL = "behavioral"
    SYSTEM = "system"


class AbuseEventEnum(StreetNinjaEnum):

    MALICIOUS = "malicious"
    INTERNATIONAL_NUMBER = "international_number"
    VOIP_NUMBER = "voip_number"
    BLOCKED_NUMBER_RETRY = "blocked_number_retry"
    
    
class AbuseEventSourceEnum(StreetNinjaEnum):
    
    PREFLIGHT = "preflight"
    POST_ANALYSIS = "post_analysis"
    
