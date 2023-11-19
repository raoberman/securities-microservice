import pandas as pd
import json

def get_data_service():
   

    config = {
        "data_directory": "./test_data",
        "data_file": "sample_stock_data.json"
    }
    data_dir = config['data_directory']
    data_file = config["data_file"]

    path = open(data_dir + "/" + data_file)

    ds = pd.read_json(path, orient = 'records')

    return ds

def get_security_by_ticker_pandas(ticker: str):
        ds = get_data_service()
        #cursor = self.cursor()
        #cursor.execute(f"SELECT ticker, stock_name, current_price FROM sample_stock_data WHERE ticker = {ticker}")
        
        result = ds.loc[ds["ticker"] == ticker].drop_duplicates(subset='ticker', keep="first")
        result = result[["ticker", "stock_name", "current_price"]].reset_index(drop = True).to_dict(orient='records')
        print(type(result))
        

        # result["ticker"] = result["ticker"].astype(str)
        # result["stock_name"] = result["stock_name"].astype(str)
        # result["current_price"] = result["current_price"].astype(float)

        
        return result