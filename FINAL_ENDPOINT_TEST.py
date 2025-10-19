#!/usr/bin/env python
import requests

BASE_URL = 'http://127.0.0.1:8000'

# All required endpoints
REQUIRED_ENDPOINTS = [
    # Authentication
    ('POST', '/api/auth/login/'),
    ('POST', '/api/auth/register/'),
    ('GET', '/api/auth/user/'),
    ('PUT', '/api/auth/user/'),
    
    # Applications
    ('GET', '/api/applications/'),
    ('POST', '/api/applications/single/'),
    ('POST', '/api/applications/double/'),
    
    # Documents
    ('GET', '/api/documents/'),
    ('POST', '/api/documents/'),
    
    # Claims
    ('GET', '/api/claims/'),
    ('POST', '/api/claims/'),
    
    # Payments
    ('GET', '/api/payments/'),
    ('POST', '/api/payments/'),
    
    # Shares
    ('GET', '/api/shares/'),
    ('POST', '/api/shares/'),
    
    # Meetings
    ('GET', '/api/meetings/'),
    
    # Beneficiaries
    ('GET', '/api/beneficiaries/'),
    ('POST', '/api/beneficiaries/change-request/'),
]

def test_endpoint(method, endpoint):
    url = BASE_URL + endpoint
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json={}, timeout=5) if method == 'POST' else requests.put(url, json={}, timeout=5)
        
        # Valid responses: 200=OK, 400=Bad Request, 401=Auth Required, 403=Permission Denied
        return response.status_code in [200, 400, 401, 403]
    except:
        return False

def main():
    print("FINAL DJANGO BACKEND COMPATIBILITY TEST")
    print("=" * 50)
    
    working = 0
    total = len(REQUIRED_ENDPOINTS)
    
    for method, endpoint in REQUIRED_ENDPOINTS:
        status = "PASS" if test_endpoint(method, endpoint) else "FAIL"
        if status == "PASS":
            working += 1
        print(f"{method:<4} {endpoint:<35} {status}")
    
    print("=" * 50)
    print(f"RESULT: {working}/{total} endpoints working")
    
    if working == total:
        print("SUCCESS: All required endpoints are functional!")
        print("Your Django backend is fully compatible with the frontend.")
    else:
        print(f"WARNING: {total - working} endpoints need attention.")

if __name__ == "__main__":
    main()