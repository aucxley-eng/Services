import unittest
import json
from app import create_app, db
from app.models import User, Product

class ProductTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Create a user and log them in to get a token
            user = User(name="Admin", email="admin@kanban.com", role="admin")
            user.set_password("admin")
            db.session.add(user)
            db.session.commit()
            
            # Simulate login to get token
            login_resp = self.client.post('/api/auth/login',
                data=json.dumps({"email": "admin@kanban.com", "password": "admin"}),
                content_type='application/json'
            )
            self.token = json.loads(login_resp.data)['access_token']

    def test_create_product(self):
        response = self.client.post('/api/products/',
            headers={"Authorization": f"Bearer {self.token}"},
            data=json.dumps({
                "name": "Maggi",
                "buying_price": 10.0,
                "product_id": "123"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()