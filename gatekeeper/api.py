from ninja import Router
from ninja.responses import Response
from django.http import HttpRequest
import logging
from typed_api_response import build_api_response
from .preflight.service import PreflightService
from .preflight.schemas import PreflightRequestData

logger = logging.getLogger(__name__)
router = Router()


@router.post("/preflight")
def predict(request: HttpRequest, data: PreflightRequestData):

    service = PreflightService(data)    
    service.run_checks()


    return Response({"foo":"bar"})





@router.post("/unresolved")
def unresolved(request: HttpRequest):
    
    return Response({"foo":"bar"})