from fastapi import Request
from fastapi.responses import JSONResponse


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 400, code: str = "error"):
        self.message = message
        self.status_code = status_code
        self.code = code


async def api_exception_handler(request: Request, exc: APIError):
    return JSONResponse(status_code=exc.status_code, content={
        "error": {
            "code": exc.code,
            "message": exc.message,
            "request_id": getattr(request.state, "request_id", None),
        }
    })
