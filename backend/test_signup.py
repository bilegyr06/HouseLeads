"""
Test script for signup endpoint with detailed logging
"""
import requests
import json

# Test 1: Valid new user signup
print("=" * 60)
print("TEST 1: Valid new user signup")
print("=" * 60)

data = {
    "email": "newtestuser@gmail.com",
    "password": "ValidPassword123@",
    "full_name": "New Test User",
    "phone_number": "08099999999",
    "location_area": "Ikoyi"
}

response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/signup",
    json=data
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
print()

# Test 2: Duplicate email
print("=" * 60)
print("TEST 2: Duplicate email")
print("=" * 60)

data2 = {
    "email": "newtestuser@gmail.com",  # Same as first test
    "password": "AnotherPassword123@",
    "full_name": "Another User",
    "phone_number": "08099998888",
    "location_area": "Lagos"
}

response2 = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/signup",
    json=data2
)

print(f"Status Code: {response2.status_code}")
print(f"Response: {json.dumps(response2.json(), indent=2)}")
