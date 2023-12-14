import typing
from typing import Optional
import strawberry
from graphql_stuff.conn.db import conn
from graphql_stuff.models.index import stocks
from strawberry.types import Info

@strawberry.type
class Stock:
    ticker: str
    current_price: float
    perf_1_mo: Optional[float]
    perf_3_mo: Optional[float]
    perf_6_mo: Optional[float]
    perf_1_year: Optional[float]
    year_min: Optional[float]
    year_max: Optional[float]


@strawberry.type
class Query:
    #resolver
    @strawberry.field
    def getStockInfoByTicker(self, info, ticker: str) -> Stock:
        return conn.execute(stocks.select().where(stocks.c.ticker == ticker)).fetchone()
    #resolver
    @strawberry.field
    def getMultipleStocksInfo(self, info, limit: int = 10) -> typing.List[Stock]:
        return conn.execute(stocks.select().limit(limit)).fetchall()
    

    #example query:
#     query Ex{
#   user(ticker:"INTC"){
#     currentPrice
#     yearMin
#     yearMax
#   }
# }

# query Ex{
#   users{
    #ticker
#     currentPrice
#     yearMin
#     yearMax
#   }
# }


