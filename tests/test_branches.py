import pytest


class TestBranchesAPI:
    """Test branch endpoints"""
    
    def test_create_branch_admin(self, client, admin_token):
        """Test admin can create branch"""
        resp = client.post('/api/branches/', 
            json={'name': 'New Branch', 'location': 'Nairobi'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert resp.status_code == 201
        assert resp.get_json()['data']['name'] == 'New Branch'
    
    def test_create_branch_manager_forbidden(self, client, manager_token):
        """Test manager cannot create branch"""
        resp = client.post('/api/branches/', 
            json={'name': 'Manager Branch'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403
    
    def test_create_branch_staff_forbidden(self, client, staff_token):
        """Test staff cannot create branch"""
        resp = client.post('/api/branches/', 
            json={'name': 'Staff Branch'},
            headers={'Authorization': f'Bearer {staff_token}'})
        assert resp.status_code == 403
    
    def test_create_branch_unauthenticated(self, client):
        """Test unauthenticated cannot create branch"""
        resp = client.post('/api/branches/', json={'name': 'Test'})
        assert resp.status_code == 401
    
    def test_get_all_branches(self, client, admin_token, auth_headers):
        """Test getting all branches"""
        client.post('/api/branches/', json={'name': 'Branch 1'}, headers=auth_headers)
        client.post('/api/branches/', json={'name': 'Branch 2'}, headers=auth_headers)
        
        resp = client.get('/api/branches/', headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.get_json()['data']['branches']) >= 2
    
    def test_get_single_branch(self, client, admin_token, auth_headers, sample_branch):
        """Test getting single branch"""
        resp = client.get(f'/api/branches/{sample_branch}', headers=auth_headers)
        assert resp.status_code == 200
        assert 'name' in resp.get_json()['data']
    
    def test_get_nonexistent_branch(self, client, auth_headers):
        """Test getting non-existent branch"""
        resp = client.get('/api/branches/9999', headers=auth_headers)
        assert resp.status_code == 404
    
    def test_update_branch_admin(self, client, admin_token, auth_headers, sample_branch):
        """Test admin can update branch"""
        resp = client.put(f'/api/branches/{sample_branch}',
            json={'name': 'Updated Branch', 'location': 'Mombasa'},
            headers=auth_headers)
        assert resp.status_code == 200
        assert resp.get_json()['data']['name'] == 'Updated Branch'
    
    def test_update_branch_manager_forbidden(self, client, manager_token, sample_branch):
        """Test manager cannot update branch"""
        resp = client.put(f'/api/branches/{sample_branch}',
            json={'name': 'Hacked'},
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403
    
    def test_delete_branch_admin(self, client, admin_token, auth_headers, sample_branch):
        """Test admin can delete branch"""
        resp = client.delete(f'/api/branches/{sample_branch}', headers=auth_headers)
        assert resp.status_code == 200
    
    def test_delete_branch_manager_forbidden(self, client, manager_token, auth_headers):
        """Test manager cannot delete branch"""
        resp = client.post('/api/branches/', json={'name': 'To Delete'}, headers=auth_headers)
        branch_id = resp.get_json().get('data', {}).get('id', 1)
        resp = client.delete(f'/api/branches/{branch_id}', 
            headers={'Authorization': f'Bearer {manager_token}'})
        assert resp.status_code == 403