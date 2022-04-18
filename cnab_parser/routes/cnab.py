from typing import List

from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, File, UploadFile, Depends

from cnab_parser.models import get_db
from cnab_parser.modules.cnab import CNAB

router = APIRouter()


@router.post("/upload")
async def create_upload_files(
    db: Session = Depends(get_db),
    files: List[UploadFile] = File(..., description="CNAB File to upload")
):
    return [
        {
            "filename": file.filename,
            "transactions": CNAB(db, file.file.read().decode('utf-8')).parser().transactions
        } for file in files
    ]


@router.get("/upload")
async def main():
    content = """
<body>
<form action="/cnab/upload" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)