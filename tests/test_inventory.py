# tests/test_inventory.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import create_app, db
from app.models.inventory import Inventory
from app.models.pharmacy import Pharmacy
from app.models.medication import Medication
from datetime import datetime

class InventoryModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a sample pharmacy and medication for testing
        self.pharmacy = Pharmacy(name="Test Pharmacy", location="Test Location", phone_number="1234567890", established_year="2023", license_number="LIC123456", owner_id=1)
        self.medication = Medication(name="Test Medication", description="Test Description", manufacturer="Test Manufacturer")
        db.session.add(self.pharmacy)
        db.session.add(self.medication)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_inventory_item(self):
        inventory_item = Inventory(
            pharmacy_id=self.pharmacy.id,
            medication_id=self.medication.id,
            quantity=100,
            unit_price=10.0,
            manufacturer="Test Manufacturer",
            manufacturing_date=datetime(2023, 1, 1),
            expiration_date=datetime(2024, 1, 1),
            shelf_number="A1",
            bin_card="Bin Card A",
            score_card="Score Card A",
            dosage_unit="mg",
            dosage_value=500
        )
        db.session.add(inventory_item)
        db.session.commit()

        retrieved_item = Inventory.query.get(inventory_item.inventory_id)
        self.assertIsNotNone(retrieved_item)
        self.assertEqual(retrieved_item.quantity, 100)
        self.assertEqual(retrieved_item.unit_price, 10.0)
        self.assertEqual(retrieved_item.manufacturer, "Test Manufacturer")

    def test_update_inventory_item(self):
        inventory_item = Inventory(
            pharmacy_id=self.pharmacy.id,
            medication_id=self.medication.id,
            quantity=100,
            unit_price=10.0,
            manufacturer="Test Manufacturer",
            manufacturing_date=datetime(2023, 1, 1),
            expiration_date=datetime(2024, 1, 1),
            shelf_number="A1",
            bin_card="Bin Card A",
            score_card="Score Card A",
            dosage_unit="mg",
            dosage_value=500
        )
        db.session.add(inventory_item)
        db.session.commit()

        # Update the inventory item
        inventory_item.quantity = 150
        inventory_item.unit_price = 12.0
        db.session.commit()

        updated_item = Inventory.query.get(inventory_item.inventory_id)
        self.assertEqual(updated_item.quantity, 150)
        self.assertEqual(updated_item.unit_price, 12.0)

    def test_delete_inventory_item(self):
        inventory_item = Inventory(
            pharmacy_id=self.pharmacy.id,
            medication_id=self.medication.id,
            quantity=100,
            unit_price=10.0,
            manufacturer="Test Manufacturer",
            manufacturing_date=datetime(2023, 1, 1),
            expiration_date=datetime(2024, 1, 1),
            shelf_number="A1",
            bin_card="Bin Card A",
            score_card="Score Card A",
            dosage_unit="mg",
            dosage_value=500
        )
        db.session.add(inventory_item)
        db.session.commit()

        # Delete the inventory item
        db.session.delete(inventory_item)
        db.session.commit()

        deleted_item = Inventory.query.get(inventory_item.inventory_id)
        self.assertIsNone(deleted_item)

if __name__ == '__main__':
    unittest.main()