__version__ = "0.0.1"

import sys
import uuid
import time

from loguru import logger
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from cnab_parser.routes import cnab, store
from cnab_parser.models.type import TypeModel
from cnab_parser.models.store import StoreModel
from cnab_parser.routes.api import include_api_routes
from cnab_parser.models.transaction import TransactionModel
from cnab_parser.exceptions import CNABParserException

app = FastAPI(
    title="CNAB Parser",
    version=__version__,
    docs_url="/swagger",
    redoc_url="/docs",
)

logger.add(sys.stdout, colorize=True, format="{time} {level} {message}", level="INFO")

include_api_routes(app)
app.include_router(cnab.router, prefix="/cnab", tags=["cnab"])
app.include_router(store.router, prefix="/store", tags=["store"])

@app.middleware("http")
async def observability(request: Request, call_next):
    id = uuid.uuid1()

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    logger.info(
        f"[{request.method}] ID: {id} - IP: {request.client.host}"
        + f" - ENDPOINT: {request.url.path} - EXCECUTION TIME: {process_time}"
    )
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.exception_handler(CNABParserException)
async def fluency_academy_assesment_exception_handler(request: Request, exception: CNABParserException):
    return JSONResponse(
        status_code=exception.status_code,
        content={"status": exception.status_code, "message": exception.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"status": 422, "message": "Invalid Request Field"},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exception: HTTPException):
    message = {401: "Not Authorize", 404: "Not Found", 405: "Method Not Allowd"}
    return JSONResponse(
        status_code=exception.status_code,
        content={"status": exception.status_code, "message": message[exception.status_code]},
    )


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_credentials=True, allow_headers=["*"]
)
