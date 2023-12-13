from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import logging

import json
#import pandas as pd
import requests
import pymysql
import sys
#import yfinance
#from sqlalchemy import create_engine
import json
from fastapi import FastAPI, Response, HTTPException
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from .graphene_model import Base

#DATABASE_URI = "database-1.csxyhdnwgd0j.us-east-2.rds.amazonaws.com://admin"






def graphene_connect_to_stocks_db(host = "database-1.csxyhdnwgd0j.us-east-2.rds.amazonaws.com",
                        port=int(3306),
                        user="admin",
                        passw="TeamAWSome2024$",
                        database="stocks"):
        try:
            config = {
                 'host': host,
                'port':port,
                'user':user,
                'password':passw,
                'database':database
            }
            engine = create_engine("mysql+pymysql://{user}:{password}@{host}:{port}/{database}".format(**config))
            #conn = pymysql.connect(host=host, user=user, port=port, passwd=passw,db=database)
            logger.info('connection started')
            return engine
        
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}

engine = graphene_connect_to_stocks_db()     
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

