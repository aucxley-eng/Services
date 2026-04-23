import pytest


class TestCategoriesAPI:
    """Test category endpoints"""
    
    def test_create_category_admin(self, client, admin_token):
        """Test admin can create category"""
        resp = client.post('/api/categories/', 
            json={'name': 'Electronics', 'description': 'Electronic items'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 201
        assert resp.get_json()['data']['name'] == 'Electronics'
    
    def test_create_category_manager_forbidden(self, client, manager_token):
        """Test manager cannot create category"""
        resp = client.post('/api/categories/', 
            json={'name': 'Manager Category'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403
    
    def test_create_category_staff_forbidden(self, client, staff_token):
        """Test staff cannot create category"""
        resp = client.post('/api/categories/', 
            json={'name': 'Staff Category'},
            headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_create_category_duplicate(self, client, admin_token):
        """Test creating duplicate category"""
        client.post('/api/categories/', json={'name': 'Duplicate'}, headers={'Authorization': f'Bearer {admin_token}'})
        resp = client.post('/api/categories/', json={'name': 'Duplicate'}, headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 409
    
    def test_get_all_categories(self, client, auth_headers):
        """Test getting all categories"""
        resp = client.get('/api/categories/', headers=auth_headers)
        assert resp.status_code == 200
        assert 'categories' in resp.get_json()['data']
    
    def test_get_single_category(self, client, auth_headers, sample_category):
        """Test getting single category"""
        resp = client.get(f'/api/categories/{sample_category}', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_update_category(self, client, admin_token, sample_category):
        """Test admin can update category"""
        resp = client.put(f'/api/categories/{sample_category}',
            json={'name': 'Updated Category', 'description': 'Updated desc'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
    
    def test_delete_category(self, client, admin_token, sample_category):
        """Test admin can delete empty category"""
        resp = client.delete(f'/api/categories/{sample_category}', 
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200


class TestSuppliersAPI:
    """Test supplier endpoints"""
    
    def test_create_supplier_admin(self, client, admin_token):
        """Test admin can create supplier"""
        resp = client.post('/api/suppliers/', 
            json={'name': 'New Supplier', 'email': 'new@supplier.com'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 201
    
    def test_create_supplier_manager(self, client, manager_token):
        """Test manager can create supplier"""
        resp = client.post('/api/suppliers/', 
            json={'name': 'Manager Supplier', 'email': 'manager@supplier.com'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 201
    
    def test_create_supplier_staff_forbidden(self, client, staff_token):
        """Test staff cannot create supplier"""
        resp = client.post('/api/suppliers/', 
            json={'name': 'Staff Supplier'},
            headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_get_all_suppliers(self, client, auth_headers):
        """Test getting all suppliers"""
        resp = client.get('/api/suppliers/', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_update_supplier(self, client, admin_token, auth_headers):
        """Test updating supplier"""
        resp = client.post('/api/suppliers/', json={'name': 'To Update'}, headers=auth_headers)
        supplier_id = resp.get_json().get('data', {}).get('id', 1)
        resp = client.put(f'/api/suppliers/{supplier_id}',
            json={'name': 'Updated Supplier'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
    
    def test_delete_supplier_admin(self, client, admin_token, auth_headers):
        """Test admin can delete supplier"""
        resp = client.post('/api/suppliers/', json={'name': 'To Delete'}, headers=auth_headers)
        supplier_id = resp.get_json().get('data', {}).get('id', 1)
        resp = client.delete(f'/api/suppliers/{supplier_id}', 
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
    
    def test_delete_supplier_manager_forbidden(self, client, manager_token, auth_headers):
        """Test manager cannot delete supplier"""
        resp = client.post('/api/suppliers/', json={'name': 'No Delete'}, headers=auth_headers)
        supplier_id = resp.get_json().get('data', {}).get('id', 1)
        resp = client.delete(f'/api/suppliers/{supplier_id}', 
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403