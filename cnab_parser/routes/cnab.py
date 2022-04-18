from typing import List

from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, File, UploadFile, Depends, Request

from cnab_parser.models import get_db
from cnab_parser.modules.cnab import CNAB


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.post("/upload")
async def process_cnab(
    request: Request,
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(..., description="CNAB File to upload")
):

    files = [
        {
            "filename": file.filename,
            "count": CNAB(db, file.file.read().decode('utf-8')).parser().transactions
        } for file in files
    ]
    return templates.TemplateResponse(
        "cnab.html", 
        {
            "request": request,
            "files": files
        }
    )