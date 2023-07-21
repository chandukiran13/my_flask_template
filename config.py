import os
import dotenv 
dotenv.load_dotenv()

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    CACHE_TYPE = os.environ.get('CACHE_TYPE','RedisCache')
    if CACHE_TYPE == 'RedisCache':
        CACHE_REDIS_URL = os.environ.get('REDIS_URL')
    
    

