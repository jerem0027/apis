from typing import Annotated, Any

import yaml
from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKey, APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from app.models.model import *
import os

DB = os.path.join(os.environ.get("ROOT_DB"), "fake_db.yml")

with open(DB, "r+") as file:
    yaml_file = yaml.safe_load(file)

fake_db = yaml_file["consoles"]

router = APIRouter(
    prefix="/console",
    tags=["console"],
    responses={
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"status_code": 404, "message": "Not Found"}
                }
            }
        },
    }
)

# TEST Authentification
fake_passwords = ["test"]
authorizations = APIKeyHeader(name="X-c4token", auto_error=False)
async def get_api_key(api_key_header: str = Security(authorizations)):
    if api_key_header in fake_passwords:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )

# Diplay element from DB
# -> Use Class as parameters
@router.get("/", name="Get list of console", response_model=None)
async def read_items(commons: Annotated[Any, Depends(ItemsParams)]) -> list[ItemsParams]:
    response = {}
    items = fake_db[commons.skip : commons.skip + commons.limit]
    response.update({"console": items})
    return response

@router.get("/{id}", name="Get list of console from ID")
async def read_items_id(id: int, api_key: APIKey = Depends(get_api_key)):
    response = {}
    items = fake_db[id:id+1]
    response.update({"console": items})
    return response

@router.post("/", name="Post console")
async def post_items(commons: Annotated[Any, Depends(Console)]):
    fake_db.append({"name": commons.nom, "puissance": commons.puissance, "color": commons.couleur })
    return {"code": 200, "message": "console add"}

# Utilisation d'une ficher en entré
@router.post("/file", name="Post console from YAML file", response_class=JSONResponse)
async def post_file(file: UploadFile) -> dict:
    if file.content_type != "application/x-yaml":
        return "erreur type"
    console_obj = yaml.safe_load(file.file.read())
    consoles = Consoles.model_validate(console_obj)
    for console in consoles.consoles:
        fake_db.append(console)
    return {"status": [consoles.consoles]}