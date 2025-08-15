from pydantic import BaseModel


class PreflightRequestData(BaseModel):
    sms_id: int
    phone_number: str
    msg: str