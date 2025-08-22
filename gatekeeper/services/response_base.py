from abc import ABC, abstractmethod
from django.conf import settings
from typed_api_response import build_api_response, ResponseMeta
from typed_api_response.schemas import ApiResponse

class BaseResponseService(ABC):
    
    API_VERSION = settings.API_VERSION

    def response(self, status: int) -> ApiResponse:
        return build_api_response(
            status=status,
            data=self._body(),
            meta=self._meta(),
        )

    @abstractmethod
    def _body(self, **kwargs):
        pass

    @abstractmethod
    def _meta(self, **kwargs) -> ResponseMeta:
        pass
        
