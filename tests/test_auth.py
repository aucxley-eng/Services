import unittest
import json
import os
from app import create_app, db
from models import User, generate_api_key


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_kanban.db'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
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
        self.assertEqual(data['message'], "User registered successfully")
        self.assertEqual(data['user']['username'], "testuser")
        self.assertIn('api_key', data['user'])

    def test_duplicate_username(self):
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
        response = self.client.post('/api/auth/register', 
            data=json.dumps({
                "username": "testuser",
                "first_name": "Test2",
                "last_name": "User2",
                "email": "test2@example.com",
                "password": "password123"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertIn('already taken', data['message'])

    def test_login(self):
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
        
        response = self.client.post('/api/auth/login', 
            data=json.dumps({
                "email": "test@example.com",
                "password": "password123"
            }), 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('api_key', data)
        self.assertIn('user', data)


if __name__ == '__main__':
    unittest.main()