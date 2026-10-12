import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-ai-super-presentation-key-2026')
    
    raw_db_url = os.getenv('DATABASE_URL', '').strip()
    
    if raw_db_url:
        # Normalize any postgres/psycopg scheme to standard postgresql+psycopg2
        raw_db_url = re.sub(r'^(postgres|postgresql)(\+psycopg)?:\/\/', 'postgresql+psycopg2://', raw_db_url)
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # Fallback to local SQLite if DATABASE_URL is not set
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'placepro.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False