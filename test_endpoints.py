#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_endpoint(endpoint, method='GET', data=None, headers=None):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        
        print(f"{method} {endpoint}: {response.status_code}")
        if response.status_code >= 400:
            print(f"  Error: {response.text[:200]}")
        else:
            print(f"  Success: {len(response.json() if response.content else [])} items")
        return response.status_code < 400
    except Exception as e:
        print(f"{method} {endpoint}: ERROR - {str(e)}")
        return False

def main():
    print("Testing API endpoints...")
    print("=" * 50)
    
    # Test public endpoints (no auth required)
    print("\n[PUBLIC] Testing Public Endpoints:")
    test_endpoint('/announcements/')
    test_endpoint('/meetings/')
    
    # Test login
    print("\n[AUTH] Testing Authentication:")
    login_data = {'username': 'testuser', 'password': 'test123'}
    login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    if login_response.status_code == 200:
        response_data = login_response.json()
        token = response_data.get('token') or response_data.get('access')
        headers = {'Authorization': f'Bearer {token}'}
        print("[OK] Login successful")
        print(f"Token: {token[:50]}..." if token else "No token received")
        
        # Test authenticated endpoints
        print("\n[PROTECTED] Testing Authenticated Endpoints:")
        test_endpoint('/claims/', headers=headers)
        test_endpoint('/contact/', headers=headers)
        test_endpoint('/applications/', headers=headers)
        test_endpoint('/payments/', headers=headers)
        test_endpoint('/shares/', headers=headers)
        test_endpoint('/documents/', headers=headers)
        test_endpoint('/beneficiaries/', headers=headers)
        
        # Test creating a claim
        print("\n[CREATE] Testing Claim Creation:")
        claim_data = {
            'claim_type': 'medical',
            'member_name': 'Test User',
            'relationship': 'self',
            'amount_requested': '100.00',
            'incident_date': '2025-10-15',
            'description': 'Test medical claim'
        }
        test_endpoint('/claims/', method='POST', data=claim_data, headers=headers)
        
    else:
        print(f"[ERROR] Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
        # Try with admin user
        print("\n[RETRY] Trying with admin user:")
        admin_login_data = {'username': 'admin', 'password': 'admin123'}
        admin_response = requests.post(f"{BASE_URL}/auth/login/", json=admin_login_data)
        
        if admin_response.status_code == 200:
            response_data = admin_response.json()
            token = response_data.get('token') or response_data.get('access')
            headers = {'Authorization': f'Bearer {token}'}
            print("[OK] Admin login successful")
            
            # Test with admin token
            print("\n[ADMIN] Testing with Admin Token:")
            test_endpoint('/claims/', headers=headers)
            test_endpoint('/contact/', headers=headers)
        else:
            print(f"[ERROR] Admin login also failed: {admin_response.status_code}")
            return

if __name__ == '__main__':
    main()