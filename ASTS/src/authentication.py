# Filename: authentication.py

import hashlib
import pyotp

def authenticate(username, password):
    # Replace with actual user data source
    stored_user_data = {
        "username": "test_user",
        "password_hash": hashlib.sha256("test_password".encode()).hexdigest()
    }
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if username == stored_user_data["username"] and password_hash == stored_user_data["password_hash"]:
        return True
    return False

def generate_2fa_code(secret):
    totp = pyotp.TOTP(secret)
    return totp.now()

def verify_2fa_code(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

# Example usage
if __name__ == "__main__":
    secret = "JBSWY3DPEHPK3PXP"  # This should be a secret key specific to each user
    token = generate_2fa_code(secret)
    print(f"Generated 2FA code: {token}")
    is_valid = verify_2fa_code(secret, token)
    print(f"Is the 2FA code valid? {is_valid}")
