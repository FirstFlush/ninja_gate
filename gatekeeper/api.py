from ninja import Router
from ninja.responses import Response
from django.http import HttpRequest
import logging
from typed_api_response import build_api_response


logger = logging.getLogger(__name__)
router = Router()


@router.post("/preflight")
def predict(request: HttpRequest):

    return Response({"bleh":"blah"})



@router.post("/unresolved")
def unresolved(request: HttpRequest):
    
    return Response({"foo":"bar"})