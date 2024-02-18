# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from starlette.testclient import TestClient

from app.api import app


def test_docs_redirect():
    client = TestClient(app)
    response = client.get("/")
    assert response.history[0].status_code == 307
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


def test_api():
    client = TestClient(app)

    # example from spacy/lang/ja/examples.py
    text = "アップルがイギリスの新興企業を１０億ドルで購入を検討"

    request_data = {"values": [{"recordId": "a1", "data": {"text": text}}]}

    response = client.post("/entities", json=request_data)
    assert response.status_code == 200

    first_record = response.json()["values"][0]
    assert first_record["recordId"] == "a1"
    assert first_record["errors"] == None
    assert first_record["warnings"] == None

    assert [entity["name"] for entity in first_record["data"]["entities"]] == [
        "アップル",
        "イギリス",
        "１０億ドル",
    ]
