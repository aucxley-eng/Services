import unittest
import json
import os
from app import create_app, db
from models import User, Product, generate_api_key


class ProductTests(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_products.db'
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            user = User(
                username="admin",
                first_name="Admin",
                last_name="User",
                email="admin@kanban.com",
                role="admin",
                api_key=generate_api_key()
            )
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()
            
            self.api_key = user.api_key

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_create_product(self):
        response = self.client.post('/api/products/',
            headers={"X-API-Key": self.api_key},
            data=json.dumps({
                "name": "Maggi",
                "buying_price": 10.0,
                "product_id": "123"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_product_without_key(self):
        response = self.client.post('/api/products/',
            data=json.dumps({
                "name": "Maggi",
                "buying_price": 10.0
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()