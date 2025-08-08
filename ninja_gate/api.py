# ninja_brain/ninja_brain/views.py
from ninja import Router
from django.http import HttpRequest

router = Router()


@router.get("/ping")
def ping(request: HttpRequest):
    return {"ping": "PONG"}
