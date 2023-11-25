
from securities_functions.securities_model import SecuritiesModel,InfoWatchlistModel
from typing import List
import pandas as pd
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



class SecuritiesResource():
    def __init__(self, config):
        super().__init__()
        self.data_service = config["data_service"]

    def get_top10_securities_by_price(self, limit:int = 10, offset:int = 0) -> List[SecuritiesModel]:
        logger.info("In resource")
        result = self.data_service.get_top10_securities_by_price_sql(limit, offset)
        logger.info(type(result))
        #logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result 
    
    def get_security_by_ticker(self, ticker: str = None) -> SecuritiesModel:
        logger.info("In resource")
        self.data_service.update_security_by_ticker_sql(ticker)
        #result = self.data_service.get_security_by_ticker_pandas(ticker
        result = self.data_service.get_security_by_ticker_sql(ticker)
        logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result
    
    
    def get_info_watchlist_by_ticker(self, ticker: str = None) -> InfoWatchlistModel:
        logger.info("In resource")
        self.data_service.update_security_by_ticker_sql(ticker)
        result = self.data_service.get_infowatchlist_by_ticker_sql(ticker)
        logger.info(result)
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result
    
    def get_custom_search_query(self, query:str = None, limit: int = 10, page: int = 0)-> List[InfoWatchlistModel]:
        logger.info("In resource custom search!")
        result = self.data_service.custom_security_search_query(query, limit, page)
        #logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result 
        #pass
        
    
    