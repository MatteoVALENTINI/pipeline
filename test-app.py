import unittest
import io
import sys
from app import app, items  # Assurez-vous d'importer également la liste 'items'

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
 
    def test_read_page(self):
        # check if the page is loaded
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200, "La page devrait se charger correctement")

    def test_add_item(self):
        # Test adding an item
        response = self.app.post('/add', data=dict(item="Test Item"), follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertIn("Test Item", response.get_data(as_text=True), "L'item ajouté devrait être dans la réponse")

    def test_update_item(self):
        # Ajout d'un item pour la mise à jour
        self.app.post('/add', data=dict(item="Old Item"), follow_redirects=True)
        response = self.app.post('/update/0', data={"new_item":"Updated Item"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertIn("Updated Item", response.get_data(as_text=True), "L'item mis à jour devrait être dans la réponse")

    def test_delete_item(self):
        # Ajout d'un item pour la suppression
        self.app.post('/add', data=dict(item="Item to Delete"), follow_redirects=True)
        response = self.app.get('/delete/0', follow_redirects=True)
        self.assertEqual(response.status_code, 200, "Response should be 200 OK")
        self.assertNotIn("Item to Delete", response.get_data(as_text=True), "L'item supprimé ne devrait plus être dans la réponse")

if __name__ == '__main__':
    unittest.main()
