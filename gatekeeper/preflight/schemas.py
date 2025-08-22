from pydantic import BaseModel
from ..enums import ResponseAction


class PreflightRequestData(BaseModel):
    sms_id: int
    phone_number: str
    msg: str
    
    
class PreflightResponseData(BaseModel):
    action: ResponseAction
    sms_id: int