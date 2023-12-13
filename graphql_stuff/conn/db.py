from sqlalchemy import create_engine, MetaData
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
import sys



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
meta = MetaData()
conn = engine.connect() 