from typed_api_response import ResponseMeta

from ..schemas import PreflightResponseData
from ...enums import ResponseAction 
from gatekeeper.services import BaseResponseService


class PreflightResponseService(BaseResponseService):
    
    def __init__(self, action: ResponseAction, sms_id: int):
        self.action = action
        self.sms_id = sms_id
        
    def _body(self) -> PreflightResponseData:
        return PreflightResponseData(
            action=self.action,
            sms_id=self.sms_id,
        )
        
    def _meta(self) -> ResponseMeta:
        return ResponseMeta(
            method="POST",
            path="/api/gate-keeper/preflight",
            version=self.API_VERSION,
        )
        
        
    
        