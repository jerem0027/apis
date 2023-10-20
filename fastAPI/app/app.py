from fastapi import FastAPI
import routes.console as console
import app.handlers.handlers as handlers
from pydantic import ValidationError

app = FastAPI(
    title="Test Fast API",
    version="0.0.1",
    docs_url="/"
)

app.include_router(console.router)
app.add_exception_handler(ValidationError, handlers.validation_exception_handler)