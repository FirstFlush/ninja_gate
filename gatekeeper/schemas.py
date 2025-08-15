from pydantic import BaseModel
    
    
class UnresolvedAnalysisRequestData(BaseModel):
    
    sms_id: int
    msg: str
    phone_number: str
