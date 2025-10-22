from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.v1 import router as v1_router
from .core.middleware import RequestIDMiddleware, TimingMiddleware
from .core.logging import configure_logging
from .core.errors import APIError, api_exception_handler


configure_logging()

app = FastAPI(title="Quant Market Predictor API", version="0.1.0")


app.add_middleware(RequestIDMiddleware)
app.add_middleware(TimingMiddleware)

@app.exception_handler(APIError)
async def _api_error_handler(request, exc):
	return await api_exception_handler(request, exc)

app.include_router(v1_router)
