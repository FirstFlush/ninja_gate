from ninja import Router
from ninja.responses import Response
from django.http import HttpRequest
import logging
from typed_api_response import build_api_response
from .preflight.services.preflight import PreflightService
from .preflight.schemas import PreflightRequestData

logger = logging.getLogger(__name__)
router = Router()


@router.post("/preflight")
def preflight(request: HttpRequest, data: PreflightRequestData):

    service = PreflightService(data)
    response = service.main()

    return Response(response)


@router.post("/postflight")
def postflight(request: HttpRequest):
    
    return Response({"foo":"bar"})