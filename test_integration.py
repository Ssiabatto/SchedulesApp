#!/usr/bin/env python3
"""
Integration test script for SchedulesApp
Tests the basic functionality of the API endpoints
"""

import os
import sys
import time
import requests

API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000/api")


def test_health_check():
    print("- Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  OK: {data.get('message', 'API is running')}")
            return True
        print(f"  FAIL: status {response.status_code}")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_user_registration():
    print("- Testing user registration...")
    try:
        username = f"testuser_{int(time.time())}"
        user_data = {
            "username": username,
            "email": f"{username}@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "role": "auxiliary",
        }
        response = requests.post(f"{API_BASE_URL}/auth/register", json=user_data, timeout=5)
        if response.status_code == 201:
            data = response.json()
            print(f"  OK: {data.get('message', 'registered')}")
            return True
        else:
            data = response.json()
            if response.status_code == 400 and 'exists' in (data.get('message', '').lower()):
                print("  WARN: user already exists, continuing")
                return True
            print(f"  FAIL: {data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def test_user_login():
    print("- Testing user login...")
    try:
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{API_BASE_URL}/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token') or data.get('data', {}).get('access_token')
            if data.get('success') and token:
                print("  OK: login successful")
                return token
            print("  FAIL: success flag/token missing")
            return None
        else:
            try:
                data = response.json()
                print(f"  FAIL: {data.get('message', 'Unknown error')}")
            except Exception:
                print(f"  FAIL: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def test_protected_endpoint(token: str):
    print("- Testing protected endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/auth/protected", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"  OK: {data.get('message', 'Access granted')}")
            return True
        else:
            try:
                data = response.json()
                print(f"  FAIL: {data.get('message', 'Unauthorized')}")
            except Exception:
                print(f"  FAIL: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def run_integration_tests():
    print("Starting SchedulesApp Integration Tests")
    print("=" * 50)

    tests_passed = 0
    total_tests = 0

    total_tests += 1
    if test_health_check():
        tests_passed += 1

    total_tests += 1
    if test_user_registration():
        tests_passed += 1

    total_tests += 1
    token = test_user_login()
    if token:
        tests_passed += 1

        total_tests += 1
        if test_protected_endpoint(token):
            tests_passed += 1
    else:
        total_tests += 1

    print("=" * 50)
    print(f"Test Results: {tests_passed}/{total_tests} tests passed")

    if tests_passed == total_tests:
        print("All tests passed! The API is working correctly.")
        return True
    else:
        print("Some tests failed. Check the backend and database configuration.")
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)
