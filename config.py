import os
import re
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-ai-secure-secret-key-2026')
    raw_db_url = os.getenv('DATABASE_URL', '').strip()

    if raw_db_url:
        # Normalize any postgres/postgresql/psycopg2 scheme to psycopg v3 (Python 3.15 + Neon native)
        raw_db_url = re.sub(
            r'^(postgres|postgresql)(\+psycopg2?)?:\/\/',
            'postgresql+psycopg://',
            raw_db_url
        )
        SQLALCHEMY_DATABASE_URI = raw_db_url
    else:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'placepro.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }