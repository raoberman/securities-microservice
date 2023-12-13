from graphql_stuff.conn.db import meta, engine
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


users = Table('SNP500', meta,  autoload_with= engine)
# users = Table('users', meta,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('name', String(50)),
#     Column('email', String(50)),
#     Column('password', String(50)),
# )