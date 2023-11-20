
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

    def __init__(self) :
        #          host= 'localhost', 
        #          user = 'root', 
        #          password = 'password', 
        #          database = 'test', 
        #          cursorType = pymysql.cursors.DictCursor):
        # """

        # :param config: A dictionary of configuration parameters.
        # """
        super().__init__()

        #path = open(self.data_dir + "/" + self.data_file)

        #self.data = pd.read_json(path, orient = 'records')

        # # Establishing the connection 
        # connection = pymysql.connect(host=host, user=user, password=password, database=database)
        # # Creating the cursor object 
        # self.cursor = connection.cursor()
    
    def _connect_to_stocks_db(self, host = "database-1.csxyhdnwgd0j.us-east-2.rds.amazonaws.com",
                        port=int(3306),
                        user="admin",
                        passw="TeamAWSome2024$",
                        database="stocks"):
        try:
            conn = pymysql.connect(host=host, user=user, port=port, passwd=passw,db=database)
            logger.info('connection started')
            return conn
        
        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }
        
    
    def get_security_by_ticker_sql(self, ticker: str):
        conn = self._connect_to_stocks_db()

        try:
            logger.info('starting security add ticker via sql')
            
            
            
            

            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # SQL command to update multiple columns
                # Replace 'table_name', 'column1', 'column2',..., 'new_value1', 'new_value2',..., and 'desired_ticker' with your actual table and column names and values
                get_stock_sql = """
                SELECT ticker, current_price
                FROM SNP500 
                WHERE ticker = %s
                """

                # get_stock_sql = """
                # SELECT *
                # FROM SNP500 
                # WHERE ticker = %s
                # """
                
                # Execute the SQL command
                cursor.execute(get_stock_sql, ticker)
                
                logger.info("Finished executing sql")
                
                
                result = cursor.fetchone()
                logger.info(result)

            
            # Commit the changes
            conn.commit()

        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

        finally:
            
            # Close the connection
            conn.close()
            logger.info("All done")
        
        return [result]
    
    def update_security_by_ticker_sql(self, ticker: str):
        logger.info("updating price data")
        #Getting updated price for ticker from Lambda function microservice
        headers = {"x-api-key": "jHZjspQE0uA9tSL8eWwK5knja7tmnC81ekpOzGF8"}

        res = requests.post('https://dph6awgc5h.execute-api.us-east-2.amazonaws.com/default/update_stock_info_containerized',json = {"ticker":ticker},headers = headers)
        logger.info(type(res.json()))
        logger.info(res.json())
        #Using the updated price info and the number of shares bought of a given ticker to update the portfolio value for the member
        #current_ticker_info = res.json()
        #response = requests.post(f'http://ec2-13-58-213-131.us-east-2.compute.amazonaws.com:8015/api/portfolios/{member_id}/buy_stock/{ticker}',json = {"num_shares":num_shares,"price_per_share":float(current_ticker_info['current_price'])})
        
        #update the stock db with the current price TODO!!!
        logger.info("finished updating price data")
        
        return res
    
    def get_top10_securities_by_price_sql(self):
        conn = self._connect_to_stocks_db()

        try:
            logger.info('starting top10 via sql')
            
            
            
            

            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # SQL command to update multiple columns
                # Replace 'table_name', 'column1', 'column2',..., 'new_value1', 'new_value2',..., and 'desired_ticker' with your actual table and column names and values
                get_top10_stock_sql = """
                SELECT ticker, current_price
                FROM SNP500
                ORDER BY current_price DESC
                LIMIT 10
                """

                # get_stock_sql = """
                # SELECT *
                # FROM SNP500 
                # WHERE ticker = %s
                # """
                
                # Execute the SQL command
                cursor.execute(get_top10_stock_sql)
                
                logger.info("Finished executing sql")
                
                
                result = cursor.fetchall()
                logger.info(result)

            
            # Commit the changes
            conn.commit()
        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

        finally:
            
            # Close the connection
            conn.close()
            logger.info("All done")
        
        return [result]
    

    def get_infowatchlist_by_ticker_sql(self, ticker: str):
        conn = self._connect_to_stocks_db()
        try:
            logger.info('starting security infowatchlist via sql')
            
            

            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # SQL command to update multiple columns
                # Replace 'table_name', 'column1', 'column2',..., 'new_value1', 'new_value2',..., and 'desired_ticker' with your actual table and column names and values
                get_stock_sql = """
                SELECT *
                FROM SNP500 
                WHERE ticker = %s
                """

                # get_stock_sql = """
                # SELECT *
                # FROM SNP500 
                # WHERE ticker = %s
                # """
                
                # Execute the SQL command
                cursor.execute(get_stock_sql, ticker)
                
                logger.info("Finished executing sql")
                
                
                result = cursor.fetchone()
                logger.info(result)

            
            # Commit the changes
            conn.commit()

        except Exception as e:
            return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

        finally:
            
            # Close the connection
            conn.close()
            logger.info("All done")
        
        return [result]

    

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
        



