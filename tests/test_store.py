from loguru import logger
from fastapi.testclient import TestClient

from cnab_parser import app

client = TestClient(app)

def test_get_all_stores():
    response = client.get("/api/store/all")
    assert type(response.json()) is list

