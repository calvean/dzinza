#!/usr/bin/python3

from models import db
from app import app

def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_database()
    print("Database created successfully.")
