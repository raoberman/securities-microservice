from typing import List
import graphene
from graphene import ObjectType, Field, String, ID, Int
from graphene_sqlalchemy import SQLAlchemyObjectType


#from .graphene_db import get_db
from .graphene_model import UserModel 

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        #interfaces = (ObjectType,)

class Query(graphene.ObjectType):
    users = graphene.List(User)

    def resolve_users(self, info):
        query = User.get_query(info)  # SQLAlchemy query
        return query.all()

schema = graphene.Schema(query=Query)