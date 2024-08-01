from cryptography.fernet import Fernet
import json
import logging

logger = logging.getLogger(__name__)

def generate_fernet_key():
    key = Fernet.generate_key()
    logger.info("Generated new Fernet key")
    
    fernet_config = {
        "key": key.decode()
    }
    
    with open('fernet.json', 'w') as fernet_file:
        json.dump(fernet_config, fernet_file, indent=4)
    logger.info("Fernet key saved to fernet.json")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_fernet_key()
