#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_activation_fee_workflow():
    print("Testing Activation Fee Workflow...")
    print("=" * 50)
    
    # Login
    login_data = {'username': 'testuser', 'password': 'test123'}
    login_response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    
    if login_response.status_code == 200:
        token = login_response.json().get('token')
        headers = {'Authorization': f'Bearer {token}'}
        print("[OK] Login successful")
        
        # Test payment submission
        print("\n[TEST] Testing payment submission:")
        payment_data = {
            'payment_method': 'paypal',
            'payment_reference': 'TEST123456',
            'amount': '50.00'
        }
        
        payment_response = requests.post(f"{BASE_URL}/applications/submit-payment/", 
                                       json=payment_data, headers=headers)
        
        if payment_response.status_code == 200:
            print("[OK] Payment submission successful")
            print(f"Response: {payment_response.json()}")
        else:
            print(f"[ERROR] Payment submission failed: {payment_response.status_code}")
            print(f"Response: {payment_response.text}")
        
        # Test applications endpoint
        print("\n[TEST] Testing applications endpoint:")
        apps_response = requests.get(f"{BASE_URL}/applications/", headers=headers)
        
        if apps_response.status_code == 200:
            apps = apps_response.json()
            print(f"[OK] Applications retrieved: {len(apps)} items")
            for app in apps:
                print(f"  - App {app.get('id')}: Status={app.get('status')}, Payment Verified={app.get('payment_verified', False)}")
        else:
            print(f"[ERROR] Applications retrieval failed: {apps_response.status_code}")
    
    else:
        print(f"[ERROR] Login failed: {login_response.status_code}")

if __name__ == '__main__':
    test_activation_fee_workflow()