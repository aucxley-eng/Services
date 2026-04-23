import pytest


class TestProductsAPI:
    """Test product endpoints"""
    
    def test_create_product_admin(self, client, admin_token):
        """Test admin can create product"""
        resp = client.post('/api/products/', 
            json={'name': 'New Product', 'buying_price': 50, 'threshold': 10},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 201
        assert resp.get_json()['data']['name'] == 'New Product'
    
    def test_create_product_manager(self, client, manager_token):
        """Test manager can create product"""
        resp = client.post('/api/products/', 
            json={'name': 'Manager Product', 'buying_price': 30},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 201
    
    def test_create_product_staff_forbidden(self, client, staff_token):
        """Test staff cannot create product"""
        resp = client.post('/api/products/', 
            json={'name': 'Staff Product'},
            headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_create_product_missing_name(self, client, admin_token):
        """Test creating product without name"""
        resp = client.post('/api/products/', 
            json={'buying_price': 50},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 400
    
    def test_create_product_missing_price(self, client, admin_token):
        """Test creating product without buying price"""
        resp = client.post('/api/products/', 
            json={'name': 'No Price'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 400
    
    def test_create_product_negative_price(self, client, admin_token):
        """Test creating product with negative price"""
        resp = client.post('/api/products/', 
            json={'name': 'Negative', 'buying_price': -10},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 400
    
    def test_get_all_products(self, client, admin_token, auth_headers):
        """Test getting all products with pagination"""
        client.post('/api/products/', json={'name': 'Product 1', 'buying_price': 10}, headers=auth_headers)
        client.post('/api/products/', json={'name': 'Product 2', 'buying_price': 20}, headers=auth_headers)
        
        resp = client.get('/api/products/', headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['total'] >= 2
    
    def test_get_products_pagination(self, client, auth_headers):
        """Test product pagination"""
        resp = client.get('/api/products/?page=1&per_page=5', headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()['data']
        assert 'current_page' in data
        assert 'pages' in data
    
    def test_get_products_search(self, client, auth_headers):
        """Test product search"""
        resp = client.get('/api/products/?search=maggi', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_get_single_product(self, client, auth_headers, sample_product):
        """Test getting single product"""
        resp = client.get(f'/api/products/{sample_product}', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_update_product_admin(self, client, auth_headers, sample_product):
        """Test admin can update product"""
        resp = client.put(f'/api/products/{sample_product}',
            json={'name': 'Updated Product', 'selling_price': 80},
            headers=auth_headers)
        assert resp.status_code == 200
    
    def test_update_product_manager(self, client, manager_token, sample_product):
        """Test manager can update product"""
        resp = client.put(f'/api/products/{sample_product}',
            json={'name': 'Manager Updated'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 200
    
    def test_delete_product_admin(self, client, auth_headers, sample_product):
        """Test admin can delete product"""
        resp = client.delete(f'/api/products/{sample_product}', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_delete_product_manager_forbidden(self, client, manager_token, auth_headers):
        """Test manager cannot delete product"""
        resp = client.post('/api/products/', 
            json={'name': 'To Delete', 'buying_price': 10},
            headers=auth_headers)
        product_id = resp.get_json().get('data', {}).get('id', 1)
        resp = client.delete(f'/api/products/{product_id}', 
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403