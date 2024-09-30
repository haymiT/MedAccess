import unittest
import json
from app import create_app, db

class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/medaccess_test'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_register_user(self):
        response = self.client.post('/api/users/register', json={
            "userEmail": "test@example.com",
            "userPassword": "password",
            "userType": "customer"
        })
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        self.client.post('/api/users/register', json={
            "userEmail": "test@example.com",
            "userPassword": "password",
            "userType": "customer"
        })
        response = self.client.post('/api/users/login', json={
            "userEmail": "test@example.com",
            "userPassword": "password"
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
