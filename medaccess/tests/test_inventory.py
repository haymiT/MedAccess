# tests/test_inventory.py
import unittest
from app import create_app, db
from app.models import Inventory, Pharmacy, Medication
from datetime import datetime

class InventoryRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create the database and tables
        db.create_all()

        # Create test data for pharmacy and medication
        self.pharmacy = Pharmacy(
            name='Test Pharmacy', 
            location='123 Test St', 
            phone_number='1234567890', 
            established_year=2020, 
            license_number='LIC123456', 
            owner_id=1
        )
        db.session.add(self.pharmacy)

        valid_category = list(Medication.CATEGORIES)[0]
        self.medication = Medication(
            name='Test Medication', 
            description='For testing purposes', 
            category=valid_category, 
            dosage='500mg'
        )
        db.session.add(self.medication)
        db.session.commit()

        self.inventory = Inventory(
            pharmacy_id=self.pharmacy.id,
            medication_id=self.medication.id,
            quantity=50,
            unit_price=10.0,
            manufacturer="Test Manufacturer",
            manufacturing_date=datetime.now(),
            expiration_date=datetime(2025, 10, 31),
            shelf_number="A1",
            dosage_unit="mg",
            dosage_value=500
        )
        db.session.add(self.inventory)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_inventory_items(self):
        response = self.client.get('/inventory')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)  # Check if one item is returned
        self.assertEqual(data[0]['dosage_unit'], 'mg')  # Check dosage_unit

    def test_get_inventory_item(self):
        response = self.client.get(f'/inventory/{self.inventory.inventory_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('pharmacy', data)
        self.assertIn('medication', data)
        self.assertEqual(data['inventory_item']['dosage_unit'], 'mg')  # Check dosage_unit

    def test_create_inventory_item(self):
        new_item = {
            'pharmacy_id': self.pharmacy.id,
            'medication_id': self.medication.id,
            'quantity': 20,
            'unit_price': 15.0,
            'manufacturer': "New Manufacturer",
            'manufacturing_date': datetime.now().isoformat(),
            'expiration_date': datetime(2026, 10, 31).isoformat(),
            'shelf_number': "B2",
            'dosage_unit': "mg",
            'dosage_value': 500
        }
        response = self.client.post('/inventory/new', json=new_item)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Inventory item created successfully!', response.get_json()['message'])

    def test_update_inventory_item(self):
        updated_data = {
            'quantity': 30,
            'unit_price': 12.0,
            'manufacturer': "Updated Manufacturer",
            'manufacturing_date': datetime.now().isoformat(),
            'expiration_date': datetime(2026, 10, 31).isoformat(),
            'shelf_number': "C3",
            'dosage_unit': "mg",
            'dosage_value': 600
        }
        response = self.client.post(f'/inventory/{self.inventory.inventory_id}/edit', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Inventory item updated successfully!', response.get_json()['message'])

    def test_delete_inventory_item(self):
        response = self.client.post(f'/inventory/{self.inventory.inventory_id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Inventory item deleted successfully!', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
