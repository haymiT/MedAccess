# tests/test_medication.py
import unittest
from app import create_app, db
from app.models import Medication

class MedicationRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        self.app.app_context().push()

        # Initialize the database
        db.create_all()

        # Use the first valid category from Medication.CATEGORIES for consistency
        valid_category = list(Medication.CATEGORIES)[0]
        
        # Set up a test medication
        self.medication = Medication(
            name="Test Medication",
            description="Test description",
            category=valid_category,
            dosage="500mg"
        )
        db.session.add(self.medication)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_medications(self):
        response = self.client.get('/medications')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Medication', response.data)

    def test_get_medication(self):
        response = self.client.get(f'/medications/{self.medication.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test description', response.data)

    def test_create_medication(self):
        response = self.client.post('/medications/new', json={
            'name': 'New Medication',
            'description': 'New description',
            'category': list(Medication.CATEGORIES)[0],
            'dosage': '250mg'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Medication created successfully!', response.data)

    def test_update_medication(self):
        response = self.client.post(f'/medications/{self.medication.id}/edit', json={
            'name': 'Updated Medication',
            'description': 'Updated description',
            'category': list(Medication.CATEGORIES)[0],
            'dosage': '750mg'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Medication updated successfully!', response.data)

    def test_delete_medication(self):
        response = self.client.post(f'/medications/{self.medication.id}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Medication deleted successfully!', response.data)

if __name__ == '__main__':
    unittest.main()
