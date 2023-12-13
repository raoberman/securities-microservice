from fastapi import APIRouter
from graphql_stuff.conn.db import conn 
#from graphql_stuff.models.index import users
from graphql_stuff.type.user import Query
from strawberry.asgi import GraphQL
import strawberry

user = APIRouter()

schema = strawberry.Schema(Query)
graphql_app = GraphQL(schema)

user.add_route("/securities/graphql", graphql_app)