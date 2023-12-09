#!/bin/bash

# Create main project directory
mkdir -p static
mkdir -p templates
mkdir -p family_tree/
mkdir -p family_tree/models
mkdir -p family_tree/routes
mkdir -p family_tree/utils
mkdir -p family_tree/config

# Create __init__.py files
touch family_tree/__init__.py
touch family_tree/models/__init__.py
touch family_tree/routes/__init__.py
touch family_tree/utils/__init__.py
touch family_tree/config/__init__.py

# Create app.py
touch family_tree/app.py

# Create the config file
touch family_tree/config/config.py

# Create user_routes.py file
touch family_tree/routes/user_routes.py

# Create family_tree_routes.py file
touch family_tree/routes/family_tree_routes.py

# Createfamily_member_routes.py file
touch family_tree/routes/family_member_routes.py

