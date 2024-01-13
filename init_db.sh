#!/bin/bash

# Set the Flask app environment variable
export FLASK_APP=run.py

# Initialize the database (create migrations directory)
flask db init

# Create an initial migration
flask db migrate -m "Initial migration"

# Apply the migration to create the database and tables
flask db upgrade

