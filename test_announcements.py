#!/usr/bin/env python
import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

def test_announcements():
    print("Testing Announcements API...")
    print("=" * 40)
    
    # Test public access
    print("\n[TEST] Public access to announcements:")
    response = requests.get(f"{BASE_URL}/announcements/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Data type: {type(data)}")
        print(f"Data: {data}")
        if isinstance(data, list):
            print(f"Count: {len(data)}")
            for item in data:
                print(f"  - {item.get('title', 'No title')}: Active={item.get('is_active', 'N/A')}")
        elif isinstance(data, dict) and 'results' in data:
            print(f"Paginated results: {len(data['results'])}")
            for item in data['results']:
                print(f"  - {item.get('title', 'No title')}: Active={item.get('is_active', 'N/A')}")
    else:
        print(f"Error: {response.text}")
    
    # Test meetings
    print("\n[TEST] Public access to meetings:")
    response = requests.get(f"{BASE_URL}/meetings/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Data type: {type(data)}")
        if isinstance(data, list):
            print(f"Count: {len(data)}")
            for item in data:
                print(f"  - {item.get('title', 'No title')}: Date={item.get('date', 'N/A')}")
        elif isinstance(data, dict) and 'results' in data:
            print(f"Paginated results: {len(data['results'])}")
            for item in data['results']:
                print(f"  - {item.get('title', 'No title')}: Date={item.get('date', 'N/A')}")
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    test_announcements()