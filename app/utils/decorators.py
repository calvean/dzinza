# app/utils.py
"""
Utility functions for the Flask application.
"""

from functools import wraps
from flask import jsonify, session, redirect

def login_required(f):
    """
    Decorator to enforce login requirement for a route.

    Args:
        f (function): The route function to be decorated.

    Returns:
        function: Decorated function with login check.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        Inner function that checks if the user is logged in.

        Returns:
            Response: JSON response if unauthorized, else the original function result.
        """
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

