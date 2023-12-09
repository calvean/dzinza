#!/usr/bin/python3

import os

class Config:
    # Use a secret key for session management
    SECRET_KEY = 'your_secret_key'

    # Configure SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Silence the deprecation warning

    # Choose your preferred database URI based on the database you are using
    # Example URI for MySQL (replace with your MySQL credentials and database name)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/dbname'
