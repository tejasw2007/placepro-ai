import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-ai-super-presentation-key-2026')
    
    # Read database URL provided by environment or Render
    raw_db_url = os.getenv('DATABASE_URL', '').strip()
    
    # Clean and force correct PostgreSQL driver prefix
    if raw_db_url:
        if raw_db_url.startswith('postgres://'):
            raw_db_url = raw_db_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        elif raw_db_url.startswith('postgresql://'):
            raw_db_url = raw_db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        # Failsafe fallback to local SQLite so the project NEVER crashes
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'placepro.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False