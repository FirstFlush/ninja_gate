from typed_api_response.schemas import ResponseMeta
from gatekeeper.services import BaseResponseService


class PostflightResponseService(BaseResponseService):
    
    def _body(self):
        ...
        
    def _meta(self) -> ResponseMeta:
        return ResponseMeta(
            version=self.API_VERSION,
            method="POST",
            path="/api/gate-keeper/preflight",
        )