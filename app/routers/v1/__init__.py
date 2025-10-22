from fastapi import APIRouter

from .system import router as system_router
from .catalog import router as catalog_router
from .data_router import router as data_router
from .train_router import router as train_router
from .models_router import router as models_router
from .forecast_router import router as forecast_router
from .signals_router import router as signals_router
from .portfolio_router import router as portfolio_router
from .backtest_router import router as backtest_router
from .diagnostics_router import router as diagnostics_router
from .admin_router import router as admin_router

router = APIRouter(prefix="/v1")
router.include_router(system_router, prefix="", tags=["system"]) 
router.include_router(catalog_router, tags=["catalog"]) 
router.include_router(data_router, tags=["data"]) 
router.include_router(train_router, tags=["train"]) 
router.include_router(models_router, tags=["models"]) 
router.include_router(forecast_router, tags=["forecast"]) 
router.include_router(signals_router, tags=["signals"]) 
router.include_router(portfolio_router, tags=["portfolio"]) 
router.include_router(backtest_router, tags=["backtest"]) 
router.include_router(diagnostics_router, tags=["diagnostics"]) 
router.include_router(admin_router, tags=["admin"]) 
