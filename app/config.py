# app/config.py
"""
Configuration settings for the Flask application.
"""

import os

class Config:
    """
    Base configuration class.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    """
    Configuration class for testing environment.
    """
    SQLALCHEMY_DATABASE_URI = 'mysql://test:password@localhost/dzinza_test'

class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )

class ProductionConfig(Config):
    """
    Configuration class for production environment.
    """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    pass
