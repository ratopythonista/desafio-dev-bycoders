from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse

from cnab_parser.modules.cnab import CNAB

router = APIRouter()


@router.post("/upload")
async def create_upload_files(
    files: List[UploadFile] = File(..., description="CNAB File to upload")
):
    return [{"filename": file.filename, "content": CNAB(file.file.read()).transactions} for file in files]


@router.get("/")
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