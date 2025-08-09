from pydantic import BaseModel


class PreflightRequestData(BaseModel):
    
    phone_number: str
    msg: str
    
    
class UnresolvedAnalysisRequestData(BaseModel):
    
    sms_id: int
    msg: str
    phone_number: str
