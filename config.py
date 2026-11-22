import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-ai-secure-secret-key-2026')
    raw_db_url = os.getenv('DATABASE_URL', '').strip()

    if raw_db_url:
        try:
            import psycopg  # Uses pure-Python psycopg v3 on Python 3.15
            dialect = 'postgresql+psycopg://'
        except ImportError:
            dialect = 'postgresql+psycopg2://'
            # Strip channel_binding unsupported by psycopg2 2.9.9
            raw_db_url = re.sub(r'([?&])channel_binding=[^&]*&?', r'\1', raw_db_url).rstrip('?&')

        raw_db_url = re.sub(r'^(postgres|postgresql)(\+psycopg2?)?:\/\/', dialect, raw_db_url)
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'placepro.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }