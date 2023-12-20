import typing
from typing import Optional
from fastapi import Query
import strawberry
from graphql_stuff.conn.db import conn
from graphql_stuff.models.index import stocks
from strawberry.types import Info
from fastapi import HTTPException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import sys

@strawberry.type
class Stock:
    ticker: str
    current_price: float
    year_min: Optional[float]
    year_max: Optional[float]

@strawberry.type
class Query:
    #resolver
    @strawberry.field
    def getStockInfoByTicker(self, info, ticker: str) -> Stock:
        result = conn.execute(stocks.select().where(stocks.c.ticker == ticker)).fetchone()
        return result
    #resolver
    @strawberry.field
    def getMultipleStocksInfo(self, info, limit: int = 10) -> typing.List[Stock]:
        if limit > 50:
            raise HTTPException(status_code=500, detail="limit exceeded. Max number of securities is 50. please try another limit"
                              )
           
        if limit <= 0:
            raise HTTPException(status_code=500, 
                                detail='limit exceeded. Min number of securities per page is 1. please try another limit'
                              )
            
        result = conn.execute(stocks.select().limit(limit)).fetchall()
        return result
    

# query ex1 {
#   getStockInfoByTicker(ticker: "NVDA") {
#     ticker
#     currentPrice
#     yearMin
#     yearMax
#   }
# }

# query ex2 {
#   getMultipleStocksInfo(limit: 2){
#     ticker
#     currentPrice
#     yearMin
#     yearMax
#   }
# }


