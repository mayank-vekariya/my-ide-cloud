# app/config.py
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
    PUBLIC_IP_ADDRESS = '34.123.45.67'
    DBNAME = 'your_database_name'
    USER = 'your_username'
    PASSWORD = 'your_password'
    # Example for PostgreSQL
    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
