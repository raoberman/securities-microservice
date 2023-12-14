from fastapi import APIRouter
from graphql_stuff.conn.db import conn 
#from graphql_stuff.models.index import users
from graphql_stuff.type.stock import Query
from strawberry.asgi import GraphQL
import strawberry

stock = APIRouter()

schema = strawberry.Schema(Query)
graphql_app = GraphQL(schema)

stock.add_route("/securities/graphql", graphql_app)