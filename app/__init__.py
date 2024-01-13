# app/__init__.py
"""
Initialization module for the Flask application.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

""" Load environment variables from the .env file """
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """
    Function to create the Flask app.
    """

    app = Flask(__name__)
    CORS(app)

    app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevelopmentConfig'))

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import user, family_tree, family_member
    app.register_blueprint(user.user_bp)
    app.register_blueprint(family_tree.family_tree_bp)
    app.register_blueprint(family_member.family_member_bp)

    return app

