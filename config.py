import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'placepro-super-secret-key-prod-2026')
    # Defaults to PostgreSQL; fallback if DATABASE_URL is not set
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'postgresql://placepro_user:2007@localhost:5432/placepro_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False