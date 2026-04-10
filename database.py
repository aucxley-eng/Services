from flask_sqlalchemy import SQLAlchemy
import secrets
from datetime import datetime

db = SQLAlchemy()


def generate_api_key():
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)