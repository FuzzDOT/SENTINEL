from fastapi import APIRouter, Request, Response
from app import __version__
from app.core.ids import get_request_id
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()


@router.get("/health")
def health(request: Request):
    return {"status": "ok", "request_id": get_request_id(request)}


@router.get("/version")
def version():
    return {"version": __version__}


@router.get("/metrics")
def metrics():
    # expose default registry metrics; in a real app we'd register custom metrics
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
