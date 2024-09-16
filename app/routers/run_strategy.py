from fastapi import APIRouter, Depends
from typing import Annotated, Optional, List, Dict
from datetime import datetime

from app.auth.auth_bearer import JWTBearer
from app.analytics.vectorbt_service import run_strategy_handler


router = APIRouter(
    prefix="/v1/run-strategy",
    tags=["run-strategy"]
)


@router.get("/", dependencies=[Depends(JWTBearer())])
def run_custom_indicator(
    symbol: List[str],
    start_time: str,
    data: Dict[str, List[Dict]],
    end_time: str = datetime.datetime.now(),
    interval: str = 'max',
):
    
    return run_strategy_handler(symbol, start_time, data, end_time, interval)