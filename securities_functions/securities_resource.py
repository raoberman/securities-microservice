
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

    def get_top10_securities_by_price(self) -> List[SecuritiesModel]:
        logger.info("In resource")
        result = self.data_service.get_top10_securities_by_price_pandas()
        logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result

    def get_security_by_ticker(self, ticker: str = None) -> List[SecuritiesModel]:
        logger.info("In resource")
        result = self.data_service.get_security_by_ticker_pandas(ticker)
        logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result
    
    def get_security_by_ticker(self, ticker: str = None) -> List[SecuritiesModel]:
        logger.info("In resource")
        result = self.data_service.get_security_by_ticker_pandas(ticker)
        logger.info(type(result))
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result
    
    def update_security_price(self, ticker_id: str = None)  -> List[SecuritiesModel]:
        pass
    
    def get_info_watchlist_by_ticker(self, ticker: str = None) -> List[InfoWatchlistModel]:
        logger.info("In resource")
        result = self.data_service.get_infowatchlist_by_ticker_pandas(ticker)
        logger.info(result)
        logger.info("Finished in resource")
        #get_portfolio(member_id, is_benchmark)
        return result
    
    