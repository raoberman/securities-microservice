
import json
import pandas as pd
import pickle
import requests
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import pymysql
#import yfinance
from sqlalchemy import create_engine
import json

import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
#import mysql.connector



class securitiesDataService():
    #TODO: add mysql implementation

    def __init__(self, config: dict) :
        #          host= 'localhost', 
        #          user = 'root', 
        #          password = 'password', 
        #          database = 'test', 
        #          cursorType = pymysql.cursors.DictCursor):
        # """

        # :param config: A dictionary of configuration parameters.
        # """
        super().__init__()

        self.data_dir = config['data_directory']
        self.data_file = config["data_file"]

        path = open(self.data_dir + "/" + self.data_file)

        self.data = pd.read_json(path, orient = 'records')

        # # Establishing the connection 
        # connection = pymysql.connect(host=host, user=user, password=password, database=database)
        # # Creating the cursor object 
        # self.cursor = connection.cursor()
    def _add_security_by_ticker_sql(self, ticker: str):
        #TODO : if stock not found, get info and add it into DB
        pass

    def get_top10_securities_by_price_pandas(self):
        try:
            
            result = self.data.sort_values('current_price', ascending = False).drop_duplicates(subset='ticker', keep="first").head(10)
            # print("HELLO!")
            # print(result)
            result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient = "records")
            logger.info("Finished getting ticker result")
        

            return result
            

             

        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

         

    def get_security_by_ticker_pandas(self, ticker: str):
        
        #cursor = self.cursor()
        #cursor.execute(f"SELECT ticker, stock_name, current_price FROM sample_stock_data WHERE ticker = {ticker}")
        try:
                if self.data.loc[self.data["ticker"] == ticker] is not None:
                    result = self.data.loc[self.data["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
                    # print("HELLO!")
                    # print(result)
                    result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient = "records")
                    logger.info("Finished getting ticker result")
                

                    return result
                #if stock doesn't exist, add a new entry
                else:
                    self._add_security_by_ticker_sql(ticker)

                     
            
            # return {"Stock Ticker": result["ticker"], 
            #         "Stock Name": result["stock_name"], 
            #         "Current Price": result["current_price"]}

        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

    
         

    def get_security_by_ticker_sql(self, ticker: str):
            
            #cursor = self.cursor()
            #cursor.execute(f"SELECT ticker, stock_name, current_price FROM sample_stock_data WHERE ticker = {ticker}")
            try:
                if self.data.loc[self.data["ticker"] == ticker] is not None:
                    result = self.data.loc[self.data["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
                    # print("HELLO!")
                    # print(result)
                    result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient = "records")
                    logger.info("Finished getting ticker result")
                

                    return result
                
                     

                
                # return {"Stock Ticker": result["ticker"], 
                #         "Stock Name": result["stock_name"], 
                #         "Current Price": result["current_price"]}

            except Exception as e:
                return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': str(e)})
            }

    def get_infowatchlist_by_ticker_pandas(self, ticker: str):
        try:
            if self.data.loc[self.data["ticker"] == ticker] is not None:
                self.data = self.data.rename(columns={"1_mo_performance": "perf_1_mo", 
                                                      "3_mo_performance": "perf_3_mo",
                                                      "6_mo_performance": "perf_6_mo",
                                                      "1_year_performance": "perf_1_year"})
                result = self.data.loc[self.data["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
                
                # print("HELLO!")
                # print(result)
                result = result.drop(['id'], axis=1).to_dict(orient = "records")
                logger.info(result)
                
                logger.info("Finished getting info result")
            

                return result
            
                    

            
            # return {"Stock Ticker": result["ticker"], 
            #         "Stock Name": result["stock_name"], 
            #         "Current Price": result["current_price"]}

        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
        



