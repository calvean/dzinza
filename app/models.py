""" app/models.py """
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    """
    Represents a user

    Attributes:
        id (int): ID for the user.
        email (str): The email address of the user (unique).
        password (str): The hashed password of the user.
        family_trees (Relationship): One-to-many relationship with FamilyTree model.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    family_trees = db.relationship('FamilyTree', backref='user', lazy=True)

    @staticmethod
    def register_user(email, password):
        """
        Register a new user.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Raises:
            Exception: If an error occurs during registration.
        """
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password)

            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def authenticate_user(email, password):
        """
        Authenticate a user with the provided email and password.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.

        Returns:
            User: The authenticated user if successful, else None.
        """
        try:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                return user
        except Exception as e:
            raise e

    def get_user_family_trees(self):
        """
        Get all family trees associated with the user.

        Returns:
            list: List of FamilyTree objects associated with the user.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return FamilyTree.query.filter_by(user_id=self.id).all()
        except Exception as e:
            raise e

    @staticmethod
    def get_user_by_email(email):
        """
        Get a user by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The user with the specified email if found, else None.

        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            raise e


