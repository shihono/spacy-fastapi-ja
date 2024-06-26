# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from collections import defaultdict

import spacy
import srsly
from fastapi import Body, FastAPI

# from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.logger import set_logger
from app.models import (
    ENT_PROP_MAP,
    RecordsEntitiesByTypeResponse,
    RecordsRequest,
    RecordsResponse,
)
from app.spacy_extractor import SpacyExtractor

# import uvicorn

logger = set_logger(__name__)
app = FastAPI(
    title="spacy-fastapi-ja",
    version="1.0",
    description="spaCy FastAPI for Custom Cognitive Skills in Azure Search",
)

example_request = srsly.read_json("app/data/example_request.json")

model_name = "ja_core_news_sm"
nlp = spacy.load(model_name)
logger.info(f"Load spacy {model_name}")
extractor = SpacyExtractor(nlp)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(f"/docs")


@app.post("/entities", response_model=RecordsResponse, tags=["NER"])
async def extract_entities(
    body: RecordsRequest = Body(..., examples=[example_request])
):
    """Extract Named Entities from a batch of Records."""

    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)
    res = [
        {"recordId": er["id"], "data": {"entities": er["entities"]}}
        for er in entities_res
    ]
    return {"values": res}


@app.post(
    "/entities_by_type", response_model=RecordsEntitiesByTypeResponse, tags=["NER"]
)
async def extract_entities_by_type(
    body: RecordsRequest = Body(..., examples=[example_request])
):
    """Extract Named Entities from a batch of Records separated by entity label.
    This route can be used directly as a Cognitive Skill in Azure Search
    For Documentation on integration with Azure Search, see here:
    https://docs.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface
    """

    documents = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)
    res = []

    for er in entities_res:
        groupby = defaultdict(list)
        for ent in er["entities"]:
            ent_prop = ENT_PROP_MAP[ent["label"]]
            groupby[ent_prop].append(ent["name"])
        record = {"recordId": er["id"], "data": groupby}
        res.append(record)

    return {"values": res}
