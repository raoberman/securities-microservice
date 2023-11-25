
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
#import mysql.connector




class securitiesDataService():
    

    def __init__(self) :
        super().__init__()

        
    
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
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}
    
    def _check_security_exists(self, ticker:str):
        conn = self._connect_to_stocks_db()
        try:
            with conn.cursor() as cursor_check:
                logger.info("checking if row exists")
                check_query = "SELECT IF (EXISTS(SELECT ticker FROM SNP500 WHERE ticker = %s), 1,0)"

                cursor_check.execute(check_query, ticker)
                
                exists = cursor_check.fetchone()[0]
                conn.close()
                #logger.info(type(exists))
                logger.info(exists)
                logger.info(type(exists))

        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}
        
        return exists
        
    
    def get_security_by_ticker_sql(self, ticker: str):
        conn = self._connect_to_stocks_db()

        try:
            logger.info('starting securiter get via sql')
            


            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                get_stock_sql = """
                SELECT ticker, current_price
                FROM SNP500 
                WHERE ticker = %s
                """

                # Execute the SQL command
                cursor.execute(get_stock_sql, ticker)
                
                logger.info("Finished executing sql")
                
                result = cursor.fetchone()
                logger.info(result)
                # Commit the changes
                conn.commit()
                
                

            

        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}

        finally:
            
            # Close the connection
            conn.close()

            logger.info("All done")

        if result == None or len(result)==0:
            raise HTTPException(status_code=500, detail='No rows with the given ticker')
            
        
        return result
    
    def update_security_by_ticker_sql(self, ticker: str):
        logger.info("updating price data")
        #Getting updated price for ticker from Lambda function microservice
        headers = {"x-api-key": "jHZjspQE0uA9tSL8eWwK5knja7tmnC81ekpOzGF8"}

        res = requests.post('https://dph6awgc5h.execute-api.us-east-2.amazonaws.com/default/update_stock_info_containerized',json = {"ticker":ticker},headers = headers)
        logger.info(type(res.json()))
        logger.info(res.json())
        
        logger.info("finished updating price data")
        
        return res
    
    
    def get_top_securities_by_price_sql(self, limit: int = 10, offset: int = 0):
        if limit > 10:
            raise HTTPException(status_code=500, detail="limit exceeded. Max number of securities per page is 50. please try another limit"
                              )
           
        if limit <= 0:
            raise HTTPException(status_code=500, 
                                detail='limit exceeded. Min number of securities per page is 1. please try another limit'
                              )
            
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
                LIMIT %s
                OFFSET %s
                """

                
                
                # Execute the SQL command
                cursor.execute(get_top10_stock_sql, (limit, offset))
                
                logger.info("Finished executing sql")
                
                
                result = cursor.fetchall()
                logger.info(result)
                logger.info(type(result))
                

            
            # Commit the changes
            conn.commit()
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}

        finally:
            
            # Close the connection
            conn.close()
            logger.info("All done")
        
        return result
    
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
                
                # Execute the SQL command
                cursor.execute(get_stock_sql, ticker)
                
                logger.info("Finished executing sql")
                
                
                result = cursor.fetchone()
                #for sanity
                result['perf_1_mo'] = result.pop('1_mo_performance')
                result['perf_3_mo'] = result.pop('3_mo_performance')
                result['perf_6_mo'] = result.pop('6_mo_performance')
                result['perf_1_year'] = result.pop('1_year_performance')
                logger.info(result)

            
            # Commit the changes
            conn.commit()

        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}

        finally:
            
            # Close the connection
            conn.close()
            logger.info("All done")
        
        return result
    

    def custom_security_search_query(self, query: str, limit: 10, page:0):
        if limit > 50:
            raise HTTPException(status_code=500, 
                                        detail='limit exceeded. Max number of securities per page is 50. please try another limit'
                                    )
        else:
            conn = self._connect_to_stocks_db()
            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    offset = page*limit
                    if query is not None:
                        logger.info(query)
                        query_str = """SELECT * 
                                FROM SNP500 
                                WHERE """ + query
                        
                        query_str2 = """
                                 LIMIT %s
                                OFFSET %s""" 
                        query_str = query_str + query_str2
                        logger.info(query_str)
                        cursor.execute(query_str, (limit, offset))
                        result = cursor.fetchall()
                    else:
                        query_str = """SELECT * 
                                FROM SNP500 
                                LIMIT %s
                                OFFSET %s"""
                        cursor.execute(query_str, (limit,offset))
                        result = cursor.fetchall()
                    
                
                    logger.info("Finished executing sql")
                    logger.info(result)

                    if result == ():      
                        raise HTTPException(status_code=500, 
                                            detail="No rows returned with that result"
                                        )
                    if result == None:      
                        raise HTTPException(status_code=500, 
                                            detail="No rows returned with that result"
                                        )
                    
                    
                    
                    logger.info(result)

                    if isinstance(result, list):
                        for i in result:
                            i['perf_1_mo'] = i.pop('1_mo_performance')
                            i['perf_3_mo'] = i.pop('3_mo_performance')
                            i['perf_6_mo'] = i.pop('6_mo_performance')
                            i['perf_1_year'] = i.pop('1_year_performance')
                    else:
                        result['perf_1_mo'] = result.pop('1_mo_performance')
                        result['perf_3_mo'] = result.pop('3_mo_performance')
                        result['perf_6_mo'] = result.pop('6_mo_performance')
                        result['perf_1_year'] = result.pop('1_year_performance')
                        result = result

                conn.commit()
                conn.close()
                    
                if result == ():      
                    raise HTTPException(status_code=500, 
                                        detail="No rows returned with that result"
                                    )
                if result == None:      
                    raise HTTPException(status_code=500, 
                                        detail="No rows returned with that result"
                                    )
                
                
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}
            
            
        
            return result
    
    def delete_security_by_ticker_sql(self, ticker: str):
        
        conn = self._connect_to_stocks_db()
        if ticker == None:
            raise HTTPException(status_code=500, detail='No ticker given to delete')
        
        exists = self._check_security_exists(ticker)
        if exists == 0:
            logger.info("in exception for row not existing")
            
            raise HTTPException(status_code=500, 
                            detail='Ticker does not exist, cannot delete')
        else:
            logger.info('ticker does exists, starting security ticker delete via sql')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                delete_stock_sql = """
                DELETE 
                FROM SNP500 
                WHERE ticker = %s
                """

                # Execute the SQL command
                cursor.execute(delete_stock_sql, ticker)
                
                logger.info("Finished executing sql")
                
                result = cursor.fetchall()
                logger.info(result)
                # Commit the changes
                conn.commit()
                conn.close()
                
        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}
        
        
            
        
        result_string = ticker +" successfully deleted from securities DB"
        result = {'status_code':200 ,'text': str(result_string),'body':{}}
            
        
        return result
    
        
        
    def add_security_by_ticker_sql(self, ticker: str, current_price: float):
        #logger.info(type(current_price))
        #logger.info(current_price)
        if len(ticker) > 4:
            raise HTTPException(status_code=500, detail='Ticker symbol must be 1-4 characters')
        
        if current_price < float(0):
            raise HTTPException(status_code=500, detail='Current price of stock must be greater than $0.00')
        
        ticker = ticker.upper()

        current_price = round(current_price,2)

        exists = self._check_security_exists(ticker)
        if exists == 1:
            logger.info("in exception for row existing")
            
            raise HTTPException(status_code=500, 
                            detail='Ticker already exists')
        else:
            logger.info('ticker does not exist, starting security ticker add via sql')


        try:
            logger.info('starting security add ticker via sql')

                
            conn = self._connect_to_stocks_db()
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                

                add_stock_sql ="""
                    INSERT INTO SNP500(ticker, current_price) VALUES (%s, %s); 
                """

                # Execute the SQL command
                cursor.execute(add_stock_sql, (ticker, current_price))
                
                logger.info("Finished executing sql")
                
                result = cursor.fetchall()
                logger.info(result)
                # Commit the changes
                conn.commit()

                conn.close()

                logger.info("All done")
                
                

            

        except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print(e, exc_tb.tb_lineno)
                return {'status_code':500,'text': str(e),'body':{}}

        

        
        # if result == None:      
        #     raise HTTPException(status_code=500, 
        #                                 detail="Row with ticker already exists"
        #                             )
        result_string = ticker +" successfully added into securities DB with price: " + str(current_price)
        result = {'status_code':200 ,'text': str(result_string),'body':{}}
            
        
        return result
        
            

    
##### TEST PANDAS

##### NOT GOING TO WORK BC TEST DATA IS GONE
    

    # def get_top10_securities_by_price_pandas(self):
    #     try:
            
    #         result = self.data.sort_values('current_price', ascending = False).drop_duplicates(subset='ticker', keep="first").head(10)
    #         # print("HELLO!")
    #         # print(result)
    #         result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient = "records")
    #         logger.info("Finished getting ticker result")
        

    #         return result
            

             

    #     except Exception as e:
    #         return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Content-Type': 'application/json'
    #         },
    #         'body': json.dumps({'error': str(e)})
    #     }

         

    # def get_security_by_ticker_pandas(self, ticker: str):
        
    #     #cursor = self.cursor()
    #     #cursor.execute(f"SELECT ticker, stock_name, current_price FROM sample_stock_data WHERE ticker = {ticker}")
    #     try:
    #             if self.data.loc[self.data["ticker"] == ticker] is not None:
    #                 result = self.data.loc[self.data["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
    #                 # print("HELLO!")
    #                 # print(result)
    #                 result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient = "records")
    #                 logger.info("Finished getting ticker result")
                

    #                 return result
    #             #if stock doesn't exist, add a new entry
    #             else:
    #                 self._add_security_by_ticker_sql(ticker)

                     
            
    #         # return {"Stock Ticker": result["ticker"], 
    #         #         "Stock Name": result["stock_name"], 
    #         #         "Current Price": result["current_price"]}

    #     except Exception as e:
    #         return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Content-Type': 'application/json'
    #         },
    #         'body': json.dumps({'error': str(e)})
    #     }

    
         
    # def get_infowatchlist_by_ticker_pandas(self, ticker: str):
    #     try:
    #         if self.data.loc[self.data["ticker"] == ticker] is not None:
    #             self.data = self.data.rename(columns={"1_mo_performance": "perf_1_mo", 
    #                                                   "3_mo_performance": "perf_3_mo",
    #                                                   "6_mo_performance": "perf_6_mo",
    #                                                   "1_year_performance": "perf_1_year"})
    #             result = self.data.loc[self.data["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
                
    #             # print("HELLO!")
    #             # print(result)
    #             result = result.drop(['id'], axis=1).to_dict(orient = "records")
    #             logger.info(result)
                
    #             logger.info("Finished getting info result")
            

    #             return result
            
                    

            
    #         # return {"Stock Ticker": result["ticker"], 
    #         #         "Stock Name": result["stock_name"], 
    #         #         "Current Price": result["current_price"]}

    #     except Exception as e:
    #         return {
    #         'statusCode': 500,
    #         'headers': {
    #             'Content-Type': 'application/json'
    #         },
    #         'body': json.dumps({'error': str(e)})
    #     }
    
    
        



