import os
from datetime import timedelta

class Config:
    # Security Keys (Generate your own random strings for these)
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') 
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///kanban.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False