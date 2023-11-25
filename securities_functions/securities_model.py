from __future__ import annotations
from pydantic import BaseModel
from typing import List
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InfoWatchlistModel(BaseModel):
    ticker: str
    current_price: float
    perf_1_mo: float | None = None
    perf_3_mo: float | None = None
    perf_6_mo: float | None = None
    perf_1_year: float | None = None
    year_min: float | None = None
    year_max: float | None = None
    
class SecuritiesModel(BaseModel):
    ticker: str
    current_price: float



