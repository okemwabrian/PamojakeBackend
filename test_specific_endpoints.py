#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000'

# Test specific endpoints required by frontend
endpoints = {
    'AUTH': [
        ('POST', '/api/auth/login/'),
        ('POST', '/api/auth/register/'),
        ('GET', '/api/auth/user/'),
        ('PUT', '/api/auth/user/'),
    ],
    'APPLICATIONS': [
        ('GET', '/api/applications/'),
        ('POST', '/api/applications/single/'),
        ('POST', '/api/applications/double/'),
    ],
    'DOCUMENTS': [
        ('GET', '/api/documents/'),
        ('POST', '/api/documents/'),
    ],
    'CLAIMS': [
        ('GET', '/api/claims/'),
        ('POST', '/api/claims/'),
    ],
    'PAYMENTS': [
        ('GET', '/api/payments/'),
        ('POST', '/api/payments/'),
    ],
    'SHARES': [
        ('GET', '/api/shares/'),
        ('POST', '/api/shares/'),
    ],
    'MEETINGS': [
        ('GET', '/api/meetings/'),
    ],
    'BENEFICIARIES': [
        ('GET', '/api/beneficiaries/'),
    ],
}

def test_endpoint(method, endpoint):
    url = BASE_URL + endpoint
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json={}, timeout=5)
        elif method == 'PUT':
            response = requests.put(url, json={}, timeout=5)
        
        # 200=OK, 401=Auth required, 403=Permission denied, 400=Bad request are all valid
        if response.status_code in [200, 400, 401, 403]:
            return "WORKING"
        else:
            return f"ERROR ({response.status_code})"
    except requests.exceptions.ConnectionError:
        return "SERVER NOT RUNNING"
    except Exception as e:
        return f"ERROR: {str(e)}"

def main():
    print("Testing Required Django Endpoints...")
    print("=" * 60)
    
    for category, endpoint_list in endpoints.items():
        print(f"\n{category}:")
        for method, endpoint in endpoint_list:
            status = test_endpoint(method, endpoint)
            print(f"  {method:<4} {endpoint:<30} {status}")

if __name__ == "__main__":
    main()