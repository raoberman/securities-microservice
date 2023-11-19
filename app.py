from fastapi import FastAPI, Response, Query
import logging

# I like to launch directly and not use the standard FastAPI startup
import uvicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from securities_functions.securities_resource import SecuritiesResource
from securities_functions.securities_data_service import securitiesDataService
from securities_functions.securities_model import SecuritiesModel
from typing import List

app = FastAPI()

                      

def get_data_service():

    config = {
        "data_directory": "./test_data",
        "data_file": "sample_stock_data.json"
    }

    ds = securitiesDataService(config)

    return ds



@app.get("/")
async def root():
    return {"message": "This is the Merry Men Trading App Securities Microservice. Stay tuned for future updates!"}

def get_securities_resource():
    ds = get_data_service()
    config = {
        "data_service": ds
    }
    res = SecuritiesResource(config)
    return res

securities_resource = get_securities_resource()


@app.get("/securities")
async def get_security_top_10(offset: int = 0,
                      limit: int = Query(default=10, le=100)):
    logger.info("In App.py")
    result = securities_resource.get_top10_securities_by_price()
    logger.info("Pass result App.py")
    return result

@app.get("/securities/{ticker}", response_model=List[SecuritiesModel])
async def get_security_resource_by_ticker(ticker: str):
    logger.info("In App.py")
    result = securities_resource.get_security_by_ticker(ticker = ticker)
    logger.info("Pass result App.py")
    return result

@app.get("/securities/{ticker}/info_watchlist")
async def get_security_resource_info_watchlist(ticker: str):
    logger.info("In App.py")
    result = securities_resource.get_info_watchlist_by_ticker(ticker = ticker)
    logger.info("Pass result App.py")
    return result


@app.get("/securities/{ticker}/buy_security/{member_id}/{portfolio_id}")
async def buy_security_by_id(ticker: str):
    pass


@app.get("/securities/{ticker}/sell_security/{member_id}/{portfolio_id}")
async def sell_security_by_id(ticker: str):
    pass

# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"AWSome Merry Men cloud developer rao2140 says hello {name}"}


# @app.get("/hello_text/{name}")
# async def say_hello_text(name: str):
#     the_message = f"AWSome Merry Men cloud developer rao2140 says Hello {name}"
#     rsp = Response(content=the_message, media_type="text/plain")
#     return rsp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8015, log_level="info")
