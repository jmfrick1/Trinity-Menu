from cryptography.fernet import Fernet
import json

# Generate a key
key = Fernet.generate_key()

# Save the key to a file (fernet.json)
with open("fernet.json", "w") as f:
    json.dump({"key": key.decode()}, f)

print("Fernet key generated and saved to fernet.json")
