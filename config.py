import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-super-secret-key-prod-2026')
    
    raw_url = os.getenv('DATABASE_URL', 'sqlite:///placepro.db')
    
    # Render provides postgres://, which SQLAlchemy 1.4+ deprecated
    if raw_url.startswith("postgres://"):
        raw_url = raw_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = raw_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False