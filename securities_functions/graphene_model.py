from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'securities'
    ticker = Column(String(5), primary_key=True)
    current_price = Column(Float)
    year_min = Column(Float)
    year_max = Column(Float)