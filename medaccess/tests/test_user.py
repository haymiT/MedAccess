import unittest
import json
from app import create_app, db
from app.models import User
import random

# List of roles for user creation
roles = ['customer', 'pharmacy', 'supplier']

class UserRoutesTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment and create a sample user."""
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a sample user with a random role
        user = User(
            name='Test User',
            email='test@example.com',
            password='password',
            phone_number='1234567890',
            role=random.choice(roles)
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_users(self):
        """Test retrieving all users."""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_get_user(self):
        """Test retrieving a specific user by ID."""
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Test User')

    def test_create_user(self):
        """Test creating a new user with a random role."""
        random_role = random.choice(roles)  # Select a random role
        new_user = {
            'name': 'New User',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '0987654321',
            'role': random_role  # Use the randomly selected role
        }

        response = self.client.post('/users/new', json=new_user)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

    def test_update_user(self):
        """Test updating an existing user."""
        random_role = random.choice(roles)  # Select a random role
        updated_user = {
            'name': 'Updated User',
            'email': 'updated@example.com',
            'phone_number': '1112223333',
            'role': random_role  # Use the randomly selected role
        }

        response = self.client.post('/users/1/edit', json=updated_user)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

    def test_delete_user(self):
        """Test deleting a user."""
        response = self.client.post('/users/1/delete')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

    def test_filter_users_by_role(self):
        """Test filtering users by a randomly selected role."""
        role = random.choice(roles)  # Select a random role

        # Use the randomly selected role in the endpoint
        response = self.client.get(f'/users/role/{role}')
        self.assertEqual(response.status_code, 200)

        # Parse and assert the response data
        data = json.loads(response.get_data(as_text=True))
        print(f"Selected role: {role}, Response data: {data}")

        # Assert that users are found for the selected role
        self.assertTrue(len(data) > 0, f"No users found with role '{role}'")

    def test_filter_users_by_email(self):
        """Test filtering users by email."""
        response = self.client.get('/users/email/test@example.com')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_filter_users_by_phone(self):
        """Test filtering users by phone number."""
        response = self.client.get('/users/phone/1234567890')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

if __name__ == '__main__':
    unittest.main()
