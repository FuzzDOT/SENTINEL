import yaml
from fastapi import APIRouter

router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("")
def list_assets():
    with open("configs/assets.yaml","r") as f:
        cfg = yaml.safe_load(f)
    return cfg
