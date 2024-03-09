import unittest
import json
import sys
import os
sys.path.append(os.path.abspath('./app'))  # Adjust the path as needed

from app import app


class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_items(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_item(self):
        response = self.app.get('/1')
        self.assertEqual(response.status_code, 404)  # Assuming there's no item with ID 1 initially

    def test_create_item(self):
        response = self.app.post('/', json={'name': 'Test Item'})
        self.assertEqual(response.status_code, 401)  # Unauthorized access without login

    def test_update_item(self):
        response = self.app.put('/1', json={'name': 'Updated Item'})
        self.assertEqual(response.status_code, 401)  # Unauthorized access without login

    def test_delete_item(self):
        response = self.app.delete('/1')
        self.assertEqual(response.status_code, 401)  # Unauthorized access without login

    def test_login(self):
        response = self.app.post('/login', json={'user': 'admin', 'pwd': 'password'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Login successful')
    

if __name__ == '__main__':
    unittest.main()
