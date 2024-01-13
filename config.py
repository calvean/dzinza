# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')
    SQLALCHEMY_DATABASE_URI = 'mysql://test:password@localhost/dzinza_test'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'passkey')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    pass

