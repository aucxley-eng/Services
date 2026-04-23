import pytest


class TestAuthAPI:
    """Test authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        resp = client.post('/api/auth/register', json={
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'new@test.com',
            'password': 'password123',
            'role': 'admin'
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'access_token' in data['data']
        assert data['message'] == 'User registered successfully'
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields"""
        resp = client.post('/api/auth/register', json={
            'username': 'incomplete'
        })
        assert resp.status_code == 400
        assert 'error' in resp.get_json()
    
    def test_register_duplicate_email(self, client, admin_token):
        """Test registration with existing email"""
        resp = client.post('/api/auth/register', json={
            'username': 'another',
            'first_name': 'Another',
            'last_name': 'User',
            'email': 'admin@test.com',
            'password': 'password123'
        })
        assert resp.status_code == 409
    
    def test_register_short_password(self, client):
        """Test registration with short password"""
        resp = client.post('/api/auth/register', json={
            'username': 'short',
            'first_name': 'Short',
            'last_name': 'Pass',
            'email': 'short@test.com',
            'password': '123'
        })
        assert resp.status_code == 400
    
    def test_login_success(self, client, admin_token):
        """Test successful login"""
        resp = client.post('/api/auth/login', json={
            'email': 'admin@test.com',
            'password': 'password123'
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'access_token' in data['data']
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        client.post('/api/auth/register', json={
            'username': 'loginuser',
            'first_name': 'Login',
            'last_name': 'User',
            'email': 'login@test.com',
            'password': 'password123'
        })
        resp = client.post('/api/auth/login', json={
            'email': 'login@test.com',
            'password': 'wrongpassword'
        })
        assert resp.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user"""
        resp = client.post('/api/auth/login', json={
            'email': 'nobody@test.com',
            'password': 'password123'
        })
        assert resp.status_code == 401
    
    def test_get_current_user(self, client, admin_token):
        """Test getting current user info"""
        resp = client.get('/api/auth/me', 
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['data']['email'] == 'admin@test.com'
    
    def test_unauthorized_access(self, client):
        """Test accessing protected endpoint without token"""
        resp = client.get('/api/auth/me')
        assert resp.status_code == 401