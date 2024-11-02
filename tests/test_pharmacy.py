import unittest
from app import create_app, db
from app.models.pharmacy import Pharmacy
from app.models.user import User
import json

class PharmacyRoutesTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask application for testing
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create the database and tables
        db.create_all()

        # Create a test user
        self.user = User(
            name='Test Owner',
            email='owner@example.com',
            password='password',
            phone_number='1234567890',
            role='pharmacy'
        )
        db.session.add(self.user)
        db.session.commit()

        # Create a test pharmacy
        self.pharmacy = Pharmacy(
            name='Test Pharmacy',
            location='123 Test St',
            phone_number='9876543210',
            established_year=2020,
            license_number='LIC123456',
            owner_id=self.user.userId
        )
        db.session.add(self.pharmacy)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_pharmacy(self):
        """Test creating a new pharmacy."""
        new_pharmacy = {
            'name': 'New Test Pharmacy',
            'location': '456 Test Ave',
            'phone_number': '1122334455',
            'established_year': 2022,
            'license_number': 'LIC654321',
            'owner_id': self.user.userId
        }

        response = self.client.post('/pharmacies/new', json=new_pharmacy)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)
        self.assertIn('Pharmacy created successfully!', data['message'])

    def test_delete_pharmacy(self):
        """Test deleting a pharmacy."""
        response = self.client.post(f'/pharmacies/{self.pharmacy.id}/delete')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)
        self.assertIn('Pharmacy deleted successfully!', data['message'])

    def test_get_pharmacies(self):
        """Test retrieving all pharmacies."""
        response = self.client.get('/pharmacies')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Pharmacy', str(response.data))

    def test_get_pharmacy(self):
        """Test retrieving a specific pharmacy by ID."""
        response = self.client.get(f'/pharmacies/{self.pharmacy.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Pharmacy', str(response.data))

    def test_update_pharmacy(self):
        """Test updating an existing pharmacy."""
        updated_data = {
            'name': 'Updated Pharmacy',
            'location': '789 Updated Blvd',
            'phone_number': '2233445566',
            'established_year': 2023,
            'license_number': 'LIC987654',
            'owner_id': self.user.userId
        }

        response = self.client.post(f'/pharmacies/{self.pharmacy.id}/edit', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Pharmacy updated successfully!', data['message'])

if __name__ == '__main__':
    unittest.main()
