"""
Test password hashing
"""
from app.core.security import hash_password, verify_password

try:
    # Test password hashing
    password = "TestPassword123@"
    print(f"Original password: {password}")
    
    hashed = hash_password(password)
    print(f"Hashed password: {hashed[:50]}...")
    print(f"Hash successful!")
    
    # Test verification
    is_valid = verify_password(password, hashed)
    print(f"Verification result: {is_valid}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
