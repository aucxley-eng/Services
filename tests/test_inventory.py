import pytest


class TestInventoryAPI:
    """Test inventory endpoints"""
    
    def test_stock_in_admin(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test admin can add stock"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 100, 'type': 'in'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 201
        assert 'transaction_id' in resp.get_json()['data']
    
    def test_stock_in_manager(self, client, manager_token, sample_branch, sample_product):
        """Test manager can add stock"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 50, 'type': 'in'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 201
    
    def test_stock_in_staff_forbidden(self, client, staff_token, sample_branch, sample_product):
        """Test staff cannot add stock"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 10, 'type': 'in'},
            headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_stock_out(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test stock out transaction"""
        client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 100, 'type': 'in'},
            headers=auth_headers)
        
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 30, 'type': 'out', 'reason': 'Sale'},
            headers=auth_headers)
        assert resp.status_code == 201
    
    def test_stock_out_insufficient(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test stock out with insufficient quantity"""
        client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 10, 'type': 'in'},
            headers=auth_headers)
        
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 100, 'type': 'out'},
            headers=auth_headers)
        assert resp.status_code == 400
    
    def test_stock_invalid_type(self, client, admin_token, sample_branch, sample_product):
        """Test invalid transaction type"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 10, 'type': 'invalid'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 400
    
    def test_stock_invalid_product(self, client, admin_token, sample_branch):
        """Test stock with non-existent product"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': 9999, 'branch_id': sample_branch, 'quantity': 10, 'type': 'in'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 404
    
    def test_stock_invalid_branch(self, client, admin_token, sample_product):
        """Test stock with non-existent branch"""
        resp = client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': 9999, 'quantity': 10, 'type': 'in'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 404
    
    def test_get_stock_levels(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test getting stock levels"""
        client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 100, 'type': 'in'},
            headers=auth_headers)
        
        resp = client.get('/api/inventory/levels', headers=auth_headers)
        assert resp.status_code == 200
        assert 'stock_levels' in resp.get_json()['data']
    
    def test_get_stock_levels_by_branch(self, client, auth_headers, sample_branch, sample_product):
        """Test getting stock levels for specific branch"""
        resp = client.get(f'/api/inventory/levels?branch_id={sample_branch}', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_get_low_stock(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test getting low stock alerts"""
        client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 5, 'type': 'in'},
            headers=auth_headers)
        
        resp = client.get('/api/inventory/low-stock', headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
    
    def test_get_low_stock_staff_forbidden(self, client, staff_token):
        """Test staff cannot view low stock"""
        resp = client.get('/api/inventory/low-stock', headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_get_transaction_history(self, client, admin_token, auth_headers, sample_branch, sample_product):
        """Test getting transaction history"""
        client.post('/api/inventory/transaction',
            json={'product_id': sample_product, 'branch_id': sample_branch, 'quantity': 100, 'type': 'in'},
            headers=auth_headers)
        
        resp = client.get('/api/inventory/history', headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 200
        assert 'transactions' in resp.get_json()['data']