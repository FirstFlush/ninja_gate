from django.conf import settings
import phonenumbers
from phonenumbers import PhoneNumberType
from .dataclasses import ScreeningCheckData
from ..enums import RiskProfileStatus

class ScreeningChecks:
    
    allowed_number_types = {
        PhoneNumberType.FIXED_LINE,
        PhoneNumberType.FIXED_LINE_OR_MOBILE,
        PhoneNumberType.MOBILE,
    }

    @staticmethod
    def appropriate_length(data: ScreeningCheckData) -> bool:
        return settings.SMS_MIN_LENGTH <= len(data.msg) <= settings.SMS_MAX_LENGTH

    @classmethod
    def number_type(cls, data: ScreeningCheckData) -> bool:
        """Check if phone number is mobile or landline (attempts to block VoIP/commercial numbers)."""
        number_type = phonenumbers.number_type(data.parsed_number)
        return number_type in cls.allowed_number_types

    @staticmethod
    def country_code(data: ScreeningCheckData) -> bool:
        if data.parsed_number.country_code == 1:
            return True
        return False

    @staticmethod
    def area_code(data: ScreeningCheckData) -> bool:
        country = phonenumbers.region_code_for_number(data.parsed_number)
        return country == "CA"

    @staticmethod
    def risk_profile(data: ScreeningCheckData) -> bool:
        match data.profile.status:
            case RiskProfileStatus.SUSPENDED.value, RiskProfileStatus.BANNED.value:
                return False
            case _:
                return True

    # @staticmethod
    # def sqli(data: ScreeningCheckData) -> bool:
    #     return True
        
    # @staticmethod
    # def code_injection(data: ScreeningCheckData) -> bool:
    #     return True

    # @staticmethod
    # def commercial_spam(data: ScreeningCheckData) -> bool:
    #     return True