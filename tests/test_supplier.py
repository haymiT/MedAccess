import unittest
import json
from app import create_app, db
from app.models import Supplier

class SupplierRoutesTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment and create a sample supplier."""
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a sample supplier
        self.supplier = Supplier(
            name='Test Supplier',
            address='123 Supplier St',
            phone_number='1234567890',
            email='supplier@example.com',
            location='Supplier City'
        )
        db.session.add(self.supplier)
        db.session.commit()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_suppliers(self):
        """Test retrieving all suppliers."""
        response = self.client.get('/suppliers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)  # Ensure suppliers are returned

    def test_get_supplier(self):
        """Test retrieving a specific supplier by ID."""
        response = self.client.get(f'/suppliers/{self.supplier.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Test Supplier')

    def test_create_supplier(self):
        """Test creating a new supplier."""
        new_supplier = {
            'name': 'New Supplier',
            'address': '456 New Supplier St',
            'phone_number': '0987654321',
            'email': 'new_supplier@example.com',
            'location': 'New Supplier City'
        }

        response = self.client.post('/suppliers/new', json=new_supplier)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

    def test_update_supplier(self):
        """Test updating an existing supplier."""
        updated_supplier = {
            'name': 'Updated Supplier',
            'address': '789 Updated Supplier Ave',
            'phone_number': '1122334455',
            'email': 'updated_supplier@example.com',
            'location': 'Updated Supplier City'
        }

        response = self.client.post(f'/suppliers/{self.supplier.id}/edit', json=updated_supplier)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

    def test_delete_supplier(self):
        """Test deleting a supplier."""
        response = self.client.post(f'/suppliers/{self.supplier.id}/delete')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
