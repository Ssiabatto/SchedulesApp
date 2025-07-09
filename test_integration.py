#!/usr/bin/env python3
"""
Integration test script for SchedulesApp
Tests the basic functionality of the API endpoints
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['message']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_user_registration():
    """Test user registration"""
    print("🔍 Testing user registration...")
    try:
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "auxiliary"
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            print(f"✅ User registration passed: {data['message']}")
            return True
        else:
            data = response.json()
            print(f"❌ User registration failed: {data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ User registration error: {e}")
        return False

def test_user_login():
    """Test user login"""
    print("🔍 Testing user login...")
    try:
        login_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and data.get('access_token'):
                print(f"✅ Login passed: {data.get('user', {}).get('username', 'user')} logged in")
                return data['access_token']
            else:
                print(f"❌ Login failed: {data.get('message', 'No token received')}")
                return None
        else:
            data = response.json()
            print(f"❌ Login failed: {data.get('message', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_protected_endpoint(token):
    """Test a protected endpoint"""
    print("🔍 Testing protected endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/auth/protected", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Protected endpoint passed: {data['message']}")
            return True
        else:
            data = response.json()
            print(f"❌ Protected endpoint failed: {data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def run_integration_tests():
    """Run all integration tests"""
    print("🚀 Starting SchedulesApp Integration Tests")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health Check
    total_tests += 1
    if test_health_check():
        tests_passed += 1
    
    # Test 2: User Registration
    total_tests += 1
    if test_user_registration():
        tests_passed += 1
    
    # Test 3: User Login
    total_tests += 1
    token = test_user_login()
    if token:
        tests_passed += 1
        
        # Test 4: Protected Endpoint (only if login successful)
        total_tests += 1
        if test_protected_endpoint(token):
            tests_passed += 1
    else:
        total_tests += 1  # Count the protected endpoint test as attempted
    
    # Results
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The API is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Check the backend and database configuration.")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
