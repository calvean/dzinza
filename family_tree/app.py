#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import Config
from routes import user_routes, family_tree_routes, family_member_routes

app = Flask(__name__)
app.config.from_object(Config)

# Configure MySQL connection URI
# Replace 'username', 'password', 'localhost', and 'dbname' with your MySQL credentials and database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'

# Silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Register blueprints
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(family_tree_routes.family_tree_bp)
app.register_blueprint(family_member_routes.family_member_bp)

if __name__ == '__main__':
    app.run(debug=True)
