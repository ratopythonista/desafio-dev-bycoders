from fastapi import FastAPI

from cnab_parser.routes.api import cnab, store

def include_api_routes(app: FastAPI):
    app.include_router(cnab.router, prefix="/api/cnab", tags=["cnab"])
    app.include_router(store.router, prefix="/api/store", tags=["store"])