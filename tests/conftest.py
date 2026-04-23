import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def admin_token(client):
    """Create admin user and return token"""
    resp = client.post('/api/auth/register', json={
        'username': 'admin',
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@test.com',
        'password': 'password123',
        'role': 'admin'
    })
    return resp.get_json()['data']['access_token']


@pytest.fixture
def manager_token(client):
    """Create manager user and return token"""
    resp = client.post('/api/auth/register', json={
        'username': 'manager',
        'first_name': 'Manager',
        'last_name': 'User',
        'email': 'manager@test.com',
        'password': 'password123',
        'role': 'manager'
    })
    return resp.get_json()['data']['access_token']


@pytest.fixture
def staff_token(client):
    """Create staff user and return token"""
    resp = client.post('/api/auth/register', json={
        'username': 'staff',
        'first_name': 'Staff',
        'last_name': 'User',
        'email': 'staff@test.com',
        'password': 'password123',
        'role': 'staff'
    })
    return resp.get_json()['data']['access_token']


@pytest.fixture
def auth_headers(admin_token):
    """Return authorization headers for admin"""
    return {'Authorization': f'Bearer {admin_token}'}


@pytest.fixture
def sample_branch(client, admin_token):
    """Create sample branch"""
    resp = client.post('/api/branches/', 
        json={'name': 'Test Branch', 'location': 'Test Location'},
        headers={'Authorization': f'Bearer {admin_token}'})
    return resp.get_json().get('data', {}).get('id', 1)


@pytest.fixture
def sample_product(client, admin_token):
    """Create sample product"""
    resp = client.post('/api/products/', 
        json={'name': 'Test Product', 'buying_price': 50, 'threshold': 10},
        headers={'Authorization': f'Bearer {admin_token}'})
    return resp.get_json().get('data', {}).get('id', 1)


@pytest.fixture
def sample_category(client, admin_token):
    """Create sample category"""
    resp = client.post('/api/categories/', 
        json={'name': 'Test Category', 'description': 'Test Description'},
        headers={'Authorization': f'Bearer {admin_token}'})
    return resp.get_json().get('data', {}).get('id', 1)