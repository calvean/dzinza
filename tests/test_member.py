import unittest
from flask import session
from app import create_app, db
from app.models import User, FamilyTree, FamilyMember

class FamilyMemberRoutesTestCase(unittest.TestCase):
    """
    This test case class contains unit tests for the Family Member routes.
    """
    def setUp(self):
        """
        Set up the test environment
        """
        self.app = create_app()
        self.app.config.from_object('config.TestConfig')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            response = self.client.post('/api/register', json={'email': 'test5@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 201)

            user = User.query.filter_by(email='test5@example.com').first()

            family_tree = FamilyTree(name='Test Tree', description='Test Description', user_id=user.id)
            db.session.add(family_tree)
            db.session.commit()

            member1 = FamilyMember(name='John Doe', gender='Male', date_of_birth='1990-01-01', tree_id=family_tree.id)
            member2 = FamilyMember(name='Jane Doe', gender='Female', date_of_birth='1992-05-15', tree_id=family_tree.id)
            db.session.add_all([member1, member2])
            db.session.commit()

            tree1 = FamilyTree(name='Test Tree 1', description='Test Description 1', user_id=user.id)
            tree2 = FamilyTree(name='Test Tree 2', description='Test Description 2', user_id=user.id)
            db.session.add_all([tree1, tree2])
            db.session.commit()

            member1_tree1 = FamilyMember(name='John Doe', gender='Male', date_of_birth='1990-01-01', tree_id=tree1.id)
            member2_tree1 = FamilyMember(name='Jane Doe', gender='Female', date_of_birth='1992-05-15', tree_id=tree1.id)
            member1_tree2 = FamilyMember(name='Bob Smith', gender='Male', date_of_birth='1985-03-20', tree_id=tree2.id)
            member2_tree2 = FamilyMember(name='Alice Smith', gender='Female', date_of_birth='1987-08-10', tree_id=tree2.id)
            db.session.add_all([member1_tree1, member2_tree1, member1_tree2, member2_tree2])
            db.session.commit()

            response = self.client.post('/api/login', json={'email': 'test5@example.com', 'password': 'password'})
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """
        Clean up the test environment by removing the database session and dropping tables.
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_family_member(self):
        """
        Test adding a new family member to a family tree.
        """
        with self.app.test_request_context():
            data = {
                'name': 'New Member',
                'gender': 'Male',
                'date_of_birth': '1995-03-20',
                'biography': 'A new family member',
                'picture_url': 'https://example.com/new_member.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            }
            response = self.client.post('/api/family-trees/1/members', json=data)
            self.assertEqual(response.status_code, 201)

            new_member = FamilyMember.query.filter_by(name='New Member', tree_id=1).first()
            self.assertIsNotNone(new_member)

    def test_add_family_member_duplicate(self):
        """
        Test adding a duplicate family member to a family tree, expecting a failure.
        """
        with self.app.test_request_context():
            data = {
                'name': 'John Doe',
                'gender': 'Male',
                'date_of_birth': '1990-01-01',
                'biography': 'Duplicate member',
                'picture_url': 'https://example.com/duplicate.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            }
            response = self.client.post('/api/family-trees/1/members', json=data)
            self.assertEqual(response.status_code, 400)

    def test_update_family_member(self):
        """
        Test updating an existing family member in a family tree.
        """
        with self.app.test_request_context():
            member_id = FamilyMember.query.filter_by(name='John Doe', tree_id=1).first().id
            data = {
                'name': 'John Doe Jr.',
                'gender': 'Male',
                'date_of_birth': '1990-01-01',
                'biography': 'Updated biography',
                'picture_url': 'https://example.com/updated.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            }
            response = self.client.put(f'/api/family-trees/1/members/{member_id}', json=data)
            self.assertEqual(response.status_code, 200)

            updated_member = FamilyMember.query.filter_by(id=member_id).first()
            self.assertIsNotNone(updated_member)
            self.assertEqual(updated_member.name, 'John Doe Jr.')
            self.assertEqual(updated_member.biography, 'Updated biography')

    def test_update_family_member_duplicate(self):
        """
        Test updating a family member with duplicate information, expecting a failure.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'John Doe Jr.',
                'gender': 'Male',
                'date_of_birth': '1990-01-01',
                'biography': 'Initial biography',
                'picture_url': 'https://example.com/initial.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 201)

            member_id = FamilyMember.query.filter_by(name='John Doe Jr.', tree_id=1).first().id
            response = self.client.put(f'/api/family-trees/1/members/{member_id}', json={
                'name': 'Jane Doe',
                'gender': 'Female',
                'date_of_birth': '1992-05-15',
                'biography': 'Updated biography',
                'picture_url': 'https://example.com/updated.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 400)

            updated_member = FamilyMember.query.filter_by(id=member_id).first()
            self.assertIsNotNone(updated_member)
            self.assertEqual(updated_member.name, 'John Doe Jr.')
            self.assertEqual(updated_member.biography, 'Initial biography')

    def test_get_parents(self):
        """
        Test retrieving the parents of a family member.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'John Doe',
                'gender': 'Male',
                'date_of_birth': '1970-01-01',
                'biography': 'Father biography',
                'picture_url': 'https://example.com/father.jpg',
                'father_name': 'Jock Doe',
                'mother_name': 'Susan Doe'
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'Jane Doe',
                'gender': 'Female',
                'date_of_birth': '1972-05-15',
                'biography': 'Mother biography',
                'picture_url': 'https://example.com/mother.jpg',
                'father_name': 'Daniel Doe',
                'mother_name': 'Tracy Doe'
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'John Doe Jr.',
                'gender': 'Male',
                'date_of_birth': '1990-01-01',
                'biography': 'John Doe Jr. biography',
                'picture_url': 'https://example.com/john_doe_jr.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 201)

            member_id = FamilyMember.query.filter_by(name='John Doe Jr.', tree_id=1).first().id

            response = self.client.get(f'/api/family-trees/1/members/{member_id}/parents')
            self.assertEqual(response.status_code, 200)

            parents_data = response.json.get('parents')
            self.assertIsNotNone(parents_data)
            self.assertIn('father', parents_data)
            self.assertIn('mother', parents_data)

            father_data = parents_data['father']
            mother_data = parents_data['mother']

            self.assertEqual(father_data['name'], 'John Doe')
            self.assertEqual(father_data['gender'], 'Male')

            self.assertEqual(mother_data['name'], 'Jane Doe')
            self.assertEqual(mother_data['gender'], 'Female')

    def test_get_siblings(self):
        """
        Test retrieving the siblings of a family member.
        """
        with self.app.test_request_context():
            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'John Doe',
                'gender': 'Male',
                'date_of_birth': '1970-01-01',
                'biography': 'Father biography',
                'picture_url': 'https://example.com/father.jpg',
                'father_name': 'Jock Doe',
                'mother_name': 'Susan Doe'
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'Jane Doe',
                'gender': 'Female',
                'date_of_birth': '1972-05-15',
                'biography': 'Mother biography',
                'picture_url': 'https://example.com/mother.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'John Doe Jr.',
                'gender': 'Male',
                'date_of_birth': '1990-01-01',
                'biography': 'John Doe Jr. biography',
                'picture_url': 'https://example.com/john_doe_jr.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 201)

            response = self.client.post('/api/family-trees/1/members', json={
                'name': 'Jane Doe Jr.',
                'gender': 'Female',
                'date_of_birth': '1992-05-15',
                'biography': 'Jane Doe Jr. biography',
                'picture_url': 'https://example.com/jane_doe_jr.jpg',
                'father_name': 'John Doe',
                'mother_name': 'Jane Doe'
            })
            self.assertEqual(response.status_code, 201)

            member_id = FamilyMember.query.filter_by(name='John Doe Jr.', tree_id=1).first().id
            response = self.client.get(f'/api/family-trees/1/members/{member_id}/siblings')
            self.assertEqual(response.status_code, 200)

            siblings_data = response.json.get('siblings')
            self.assertIsNotNone(siblings_data)
            self.assertEqual(len(siblings_data), 2)

            sibling_names = [sibling['name'] for sibling in siblings_data]
            self.assertIn('Jane Doe', sibling_names)
            self.assertIn('Jane Doe Jr.', sibling_names)


    def test_get_all_members_in_tree(self):
        """
        Test retrieving all family members in a family tree.
        """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees/1/members')
            self.assertEqual(response.status_code, 200)

            members = response.json.get('family_members')
            self.assertIsNotNone(members)
            self.assertEqual(len(members), 2)

    def test_get_family_member(self):
        """
        Test retrieving information about a specific family member.
        """
        with self.app.test_request_context():
            member_id = FamilyMember.query.filter_by(name='John Doe', tree_id=1).first().id
            response = self.client.get(f'/api/family-trees/1/members/{member_id}')
            self.assertEqual(response.status_code, 200)

            family_member = response.json.get('family_member')
            self.assertIsNotNone(family_member)
            self.assertEqual(family_member['name'], 'John Doe')

    def test_get_family_member_not_found(self):
        """
        Test retrieving a non-existent family member, expecting a failure.
        """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees/1/members/999')
            self.assertEqual(response.status_code, 404)

    def test_delete_family_member(self):
        """
        Test deleting an existing family member.
        """
        with self.app.test_request_context():
            member_id = FamilyMember.query.filter_by(name='John Doe', tree_id=1).first().id
            response = self.client.delete(f'/api/family-trees/1/members/{member_id}')
            self.assertEqual(response.status_code, 200)

            deleted_member = FamilyMember.query.filter_by(id=member_id).first()
            self.assertIsNone(deleted_member)

    def test_delete_family_member_not_found(self):
        """
        Test deleting a non-existent family member, expecting a failure.
        """
        with self.app.test_request_context():
            response = self.client.delete('/api/family-trees/1/members/999')
            self.assertEqual(response.status_code, 404)
            

    def test_search_family_members_all_trees(self):
        """
        Test searching for family members across all family trees with a specific query.
        """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees/members/search?q=John')
            self.assertEqual(response.status_code, 200)

            search_results = response.json.get('search_results')
            self.assertIsNotNone(search_results)
            self.assertEqual(len(search_results), 3)

            result_test_tree = search_results['Test Tree']
            self.assertEqual(len(result_test_tree), 1)
            self.assertEqual(result_test_tree[0]['name'], 'John Doe')

            result_test_tree_1 = search_results['Test Tree 1']
            self.assertEqual(len(result_test_tree_1), 1)
            self.assertEqual(result_test_tree_1[0]['name'], 'John Doe')

            result_test_tree_2 = search_results['Test Tree 2']
            self.assertEqual(len(result_test_tree_2), 0)

    def test_search_family_members_all_trees_no_query(self):
        """
        Test searching for family members across all family trees without providing a query, expecting a failure.
        """
        with self.app.test_request_context():
            response = self.client.get('/api/family-trees/members/search')
            self.assertEqual(response.status_code, 400)

            error_message = response.json.get('error')
            self.assertIsNotNone(error_message)
            self.assertIn('Search query is required', error_message)

if __name__ == '__main__':
    unittest.main()
