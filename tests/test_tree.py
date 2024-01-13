import unittest
from flask import session
from app import create_app, db
from app.models import User, FamilyTree, FamilyMember

class FamilyTreeRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """ Setup Flask app and test client """
        self.app = create_app()
        self.app.config.from_object('config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            response = self.client.post('/api/register', json={'email': 'test5@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 201)

            user = User.query.filter_by(email='test5@example.com').first()

            response = self.client.post('/api/login', json={'email': 'test5@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """ Clean up database after each test """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_family_trees(self):
        """ Test retrieving family trees for the logged-in user """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees')
            self.assertEqual(response.status_code, 200)

            family_trees = response.json.get('family_trees')
            self.assertIsNotNone(family_trees)
            self.assertEqual(len(family_trees), 0)

    def test_create_family_tree(self):
        """ Test creating a new family tree """
        with self.app.test_request_context():
            data = {
                'name': 'Test Tree',
                'description': 'Test Description'
            }
            response = self.client.post('/api/family-trees', json=data)
            self.assertEqual(response.status_code, 201)

            new_tree = FamilyTree.query.filter_by(name='Test Tree').first()
            self.assertIsNotNone(new_tree)

    def test_create_duplicate_family_tree(self):
        """ Test creating a duplicate family tree """
        with self.app.test_request_context():
            data = {
                'name': 'Test Tree',
                'description': 'Test Description'
            }
            response = self.client.post('/api/family-trees', json=data)
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees', json=data)
            self.assertEqual(response.status_code, 400)

    def test_get_family_tree(self):
        """ Test retrieving information about a specific family tree """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees', json={'name': 'Test Tree', 'description': 'Test Description'})
            self.assertEqual(response.status_code, 201)

            tree_id = FamilyTree.query.filter_by(name='Test Tree').first().id
            response = self.client.get(f'/api/family-trees/{tree_id}')
            self.assertEqual(response.status_code, 200)

            family_tree = response.json.get('family_tree')
            self.assertIsNotNone(family_tree)
            self.assertEqual(family_tree['name'], 'Test Tree')

    def test_get_family_tree_not_found(self):
        """ Test retrieving a non-existent family tree """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees/999')
            self.assertEqual(response.status_code, 404)

    def test_get_all_members_in_tree(self):
        """ Test retrieving all family members in a specific family tree """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees', json={'name': 'Test Tree', 'description': 'Test Description'})
            self.assertEqual(response.status_code, 201)

            tree_id = FamilyTree.query.filter_by(name='Test Tree').first().id
            response = self.client.get(f'/api/family-trees/{tree_id}/members')
            self.assertEqual(response.status_code, 200)

            family_members = response.json.get('family_members')
            self.assertIsNotNone(family_members)
            self.assertEqual(len(family_members), 0)

    def test_update_family_tree(self):
        """ Test updating details of a specific family tree """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees', json={'name': 'Test Tree', 'description': 'Test Description'})
            self.assertEqual(response.status_code, 201)

            tree_id = FamilyTree.query.filter_by(name='Test Tree').first().id
            response = self.client.put(f'/api/family-trees/{tree_id}', json={'name': 'Updated Tree', 'description': 'Updated Description'})
            self.assertEqual(response.status_code, 200)

            updated_tree = FamilyTree.query.filter_by(id=tree_id).first()
            self.assertIsNotNone(updated_tree)
            self.assertEqual(updated_tree.name, 'Updated Tree')
            self.assertEqual(updated_tree.description, 'Updated Description')

    def test_update_family_tree_not_found(self):
        """ Test updating a non-existent family tree """
        with self.app.test_request_context():
            response = self.client.put('/api/family-trees/999', json={'name': 'Updated Tree', 'description': 'Updated Description'})
            self.assertEqual(response.status_code, 404)

    def test_delete_family_tree(self):
        """ Test deleting a specific family tree """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees', json={'name': 'Test Tree', 'description': 'Test Description'})
            self.assertEqual(response.status_code, 201)

            tree_id = FamilyTree.query.filter_by(name='Test Tree').first().id
            response = self.client.delete(f'/api/family-trees/{tree_id}')
            self.assertEqual(response.status_code, 200)

            deleted_tree = FamilyTree.query.filter_by(id=tree_id).first()
            self.assertIsNone(deleted_tree)

    def test_delete_family_tree_not_found(self):
        """ Test deleting a non-existent family tree """
        with self.app.test_request_context():
            response = self.client.delete('/api/family-trees/999')
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

