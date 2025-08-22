from pydantic import BaseModel
from gatekeeper.enums import ResponseAction


class PostflightRequestData(BaseModel):
    
    sms_id: int
    phone_number: str
    msg: str
    preflight_decision: ResponseAction