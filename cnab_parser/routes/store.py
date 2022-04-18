from typing import List

from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Path, Depends, Request

from cnab_parser.models import get_db
from cnab_parser.modules.store import StoreCRUD
from cnab_parser.modules.transaction import TransactionCRUD


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/transactions/{store_id}", response_class=HTMLResponse, include_in_schema=False)
async def store_transactions(
    request: Request,
    db: Session = Depends(get_db),
    store_id = Path(..., description="Store identifier"),
):
    transaction_list, balance = TransactionCRUD(db).get_by_store(store_id)
    return templates.TemplateResponse(
        "transactions.html", 
        {
            "request": request,
            "balance": balance,
            "transaction_list": transaction_list
        }
    )

@router.get("/all", include_in_schema=False)
def get_all_stores(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "store.html", 
        {
            "request": request,
            "store_list": StoreCRUD(db).get_all()
        }
    )