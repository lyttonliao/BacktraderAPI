from fastapi import APIRouter, Depends
from typing import Annotated, Optional

from app.auth.auth_bearer import JWTBearer


router = APIRouter(
    prefix="/v1/run-strategy",
    tags=["run-strategy"]
)


# @router.get("/", dependencies=[Depends(JWTBearer())])
# def run_custom_indicator(
#     name: str,
#     short_name: Optional[str] = None,
#     input_names: list[str],
#     param_names: list[str],
#     output_names: list[str]
# ):
    