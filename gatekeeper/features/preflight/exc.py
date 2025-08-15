
class PreflightServiceError(Exception):
    """Raised when the PreflightService fails for any reason"""
    pass

class AbuseDetectionError(PreflightServiceError):
    """Raised when the AbuseDetectionService fails encounters an unexpected error"""
    pass

class AbuseEventServiceError(PreflightServiceError):
    """Raised when the AbuseEventService fails to create the AbuseEvent records"""
    pass
