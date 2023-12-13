import typing
from typing import Optional
import strawberry
from graphql_stuff.conn.db import conn
from graphql_stuff.models.index import users
from strawberry.types import Info

@strawberry.type
class User:
    ticker: str
    current_price: float
    year_min: Optional[float]
    year_max: Optional[float]

@strawberry.type
class Query:
    #resolver
    @strawberry.field
    def user(self, info, ticker: str) -> User:
        return conn.execute(users.select().where(users.c.ticker == ticker)).fetchone()
    #resolver
    @strawberry.field
    def users(self, info) -> typing.List[User]:
        return conn.execute(users.select()).fetchall()
    

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


