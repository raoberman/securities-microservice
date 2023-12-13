from fastapi import FastAPI, Response
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp

import graphene

import logging

# I like to launch directly and not use the standard FastAPI startup
import uvicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from securities_functions.securities_resource import SecuritiesResource
from securities_functions.securities_data_service import securitiesDataService
from securities_functions.securities_model import SecuritiesModel, InfoWatchlistModel
from securities_functions.graphene_db import get_db
from securities_functions.graphene_model import UserModel 
from securities_functions.graphene_schemas import Query
from typing import List

app = FastAPI()

schema = graphene.Schema(query=Query)


def get_data_service():

    # config = {
    #     "host":"database-1.csxyhdnwgd0j.us-east-2.rds.amazonaws.com",
    #     "port":"3306",
    #     "user":"admin",
    #     "passw":"TeamAWSome2024$",
    #     "database":"stocks"
    # }

    ds = securitiesDataService()

    return ds



@app.get("/")
async def root():
    return {"message": "This is the Merry Men Trading App Securities Microservice. Stay tuned for future updates!"}

app.add_route("/securites/graphql", 
              GraphQLApp(schema=Query))                    

def get_securities_resource():
    ds = get_data_service()
    config = {
        "data_service": ds
    }
    res = SecuritiesResource(config)
    return res

securities_resource = get_securities_resource()


@app.get("/top_securities_by_price", response_model = List[SecuritiesModel])
async def get_top_securities_by_price(limit: int = 10, offset: int = 0):
    logger.info("In App.py")
    result = securities_resource.get_top_securities_by_price(limit, offset)
    logger.info("Pass result App.py")
    return result

@app.get("/securities/{ticker}", response_model = SecuritiesModel)
async def get_security_resource_by_ticker(ticker: str):
    logger.info("In App.py")
    result = securities_resource.get_security_by_ticker(ticker = ticker)
    logger.info("Pass result App.py")
    return result

@app.get("/securities/{ticker}/info_watchlist", response_model = InfoWatchlistModel)
async def get_security_resource_info_watchlist(ticker: str):
    logger.info("In App.py")
    result = securities_resource.get_info_watchlist_by_ticker(ticker = ticker)
    logger.info("Pass result App.py")
    return result


@app.get("/securities/custom_security_search/", response_model = List[InfoWatchlistModel])
async def security_custom_sql_search(query: str = None, 
                      limit: int = 10, page: int = 0):
    logger.info("In App.py")
    result = securities_resource.get_custom_search_query(query = query, limit = limit, page = page)
    logger.info("Pass result App.py")
    return result


@app.put("/securities/{ticker}/update_security_price", response_model = SecuritiesModel)
async def update_security_price(ticker: str):
    logger.info("In App.py")
    result = securities_resource.update_security_price(ticker = ticker)
    logger.info("Pass result App.py")
    return result

@app.delete("/securities/{ticker}/delete_security")
async def delete_security(ticker: str):
    logger.info("In App.py")
    result = securities_resource.delete_security_by_ticker(ticker = ticker)
    logger.info("Pass result App.py")
    return result

@app.post("/securities/{ticker}/add_security")
async def add_security(ticker: str, current_price: float = 0.00):
    logger.info("In App.py")
    result = securities_resource.add_security(ticker = ticker, current_price = current_price)
    logger.info("Pass result App.py")
    return result



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8015, log_level="info")
