import unittest
from flask import Flask
from app import app  # import your Flask app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        # Assuming you have a user with id 1
        response = self.client.post('/delete', data={'user_id': 1})
        self.assertEqual(response.status_code, 200)

    def test_new_user(self):
        response = self.client.get('/new_user')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()