import unittest
from flask import session
from app import create_app, db
from app.models import User


class UserRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment.
        - Create a test Flask app.
        - Set configurations from the TestConfig class.
        - Create a test client.
        - Create tables in the test database.
        """
        self.app = create_app()
        self.app.config.from_object('config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """
        Tear down the test environment.
        - Remove the database session.
        - Drop all tables after each test.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        """
        Test user registration.
        - Send a POST request to register a user.
        - Check if the user was added to the database.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/register', json={'email': 'test@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 201)

            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')

    def test_register_user_invalid_data(self):
        """
        Test user registration with invalid data.
        - Send a POST request with invalid data.
        - Check for a 500 Internal Server Error response.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/register', json={'email': 'invalid_email'})
            self.assertEqual(response.status_code, 500)

    def test_login_user(self):
        """
        Test user login.
        - Register a user first.
        - Send a POST request to login the user.
        - Check for a 200 OK response.
        """
        with self.app.test_request_context():
            self.client.post('/api/register', json={'email': 'test@example.com', 'password': 'password'})

        with self.app.test_request_context():
            response = self.client.post('/api/login', json={'email': 'test@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 200)

    def test_login_user_invalid_credentials(self):
        """
        Test user login with invalid credentials.
        - Send a POST request with incorrect credentials.
        - Check for a 401 Unauthorized response.
        - Check that 'user_id' is not in the session.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/login', json={'email': 'nonexistent@example.com', 'password': 'wrong_password'})
            self.assertEqual(response.status_code, 401)
            self.assertNotIn('user_id', session)

    def test_logout_user(self):
        """
        Test user logout.
        - Login a user first.
        - Send a POST request to logout the user.
        - Check for a 200 OK response.
        - Check that 'user_id' is not in the session.
        """
        with self.app.test_request_context():
            self.client.post('/api/register', json={'email': 'test@example.com', 'password': 'password'})
            self.client.post('/api/login', json={'email': 'test@example.com', 'password': 'password'})

        with self.app.test_request_context():
            response = self.client.post('/api/logout')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('user_id', session)

    def test_logout_user_not_logged_in(self):
        """
        Test user logout when not logged in.
        - Send a POST request to logout the user.
        - Check for a 401 Unauthorized response.
        - Check that 'user_id' is not in the session.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/logout')
            self.assertEqual(response.status_code, 401)
            self.assertNotIn('user_id', session)

if __name__ == '__main__':
    unittest.main()

