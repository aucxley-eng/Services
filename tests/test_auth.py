import unittest
import json
import os
from app import create_app, db

class AuthTests(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_kanban.db'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from app.models import User, Product, Branch, Category, Supplier, Stock, Order
            db.drop_all()
            db.create_all()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_register_user(self):
        response = self.client.post('/api/auth/register', 
            data=json.dumps({
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "User created successfully")
        self.assertEqual(data['user']['username'], "testuser")
        self.assertEqual(data['user']['first_name'], "Test")
        self.assertEqual(data['user']['last_name'], "User")

    def test_duplicate_registration(self):
        # Register first user
        self.client.post('/api/auth/register', 
            data=json.dumps({
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123"
            }), 
            content_type='application/json'
        )
        # Try to register same user again
        response = self.client.post('/api/auth/register', 
            data=json.dumps({
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@example.com",
                "password": "password123"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "User with this email or username already exists")

if __name__ == '__main__':
    unittest.main()
