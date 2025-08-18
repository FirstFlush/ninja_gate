from ...enums import AbuseEventTypeEnum, AbuseCategoryEnum


EVENT_TYPE_DATA = [
        {
            "name": AbuseEventTypeEnum.INTERNATIONAL_NUMBER,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
        },
        {
            "name": AbuseEventTypeEnum.INVALID_AREA_CODE,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
        },
        {
            "name": AbuseEventTypeEnum.MALICIOUS,
            "category": AbuseCategoryEnum.SECURITY,
            "description": "",
        },
        {
            "name": AbuseEventTypeEnum.VOIP_NUMBER,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
        },
        {
            "name": AbuseEventTypeEnum.COMMERCIAL_SPAM,
            "category": AbuseCategoryEnum.SECURITY,
            "description": "",
        },
        {
            "name": AbuseEventTypeEnum.UNRESOLVED_MSG,
            "category": AbuseCategoryEnum.BEHAVIORAL,
            "description": "",
        },
    ]