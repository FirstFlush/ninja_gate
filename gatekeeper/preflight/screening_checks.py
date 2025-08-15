from .schemas import PreflightRequestData


class ScreeningChecks:
        
    @staticmethod
    def voip_number(data: PreflightRequestData) -> bool:
        ...
        
    @staticmethod
    def international_number(data: PreflightRequestData) -> bool:
        ...
        
    @staticmethod
    def usa_number(data: PreflightRequestData) -> bool:
        ...
        
    @staticmethod
    def sqli(data: PreflightRequestData) -> bool:
        ...
    
    @staticmethod
    def code_injection(data: PreflightRequestData) -> bool:
        ...
    
    @staticmethod
    def commercial_spam(data: PreflightRequestData) -> bool:
        ...