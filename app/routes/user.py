""" app/routes/user.py """
from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from app.utils.decorators import login_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/register', methods=['POST'])
def register_user():
    """
    Register a new user.

    Returns:
        jsonify: JSON response with a success message.

    Raises:
        Exception: If an error occurs during user registration.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.register_user(email, password)

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/login', methods=['POST'])
def login_user():
    """
    Log in an existing user.

    Returns:
        jsonify: JSON response with a success message or error message.

    Raises:
        Exception: If an error occurs during user authentication.
    """
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.authenticate_user(email, password)

        if user:
            # Use session to store user ID after login
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/api/logout', methods=['POST'])
@login_required
def logout_user():
    """
    Log out the current user.

    Returns:
        jsonify: JSON response with a success message.

    Raises:
        Exception: If an error occurs during user logout.
    """
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

