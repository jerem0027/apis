from fastapi import Request
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError
from starlette.status import HTTP_400_BAD_REQUEST


# Handler
async def validation_exception_handler(request: Request, exc: ValidationError):
    return PlainTextResponse(str(exc), status_code=HTTP_400_BAD_REQUEST)
