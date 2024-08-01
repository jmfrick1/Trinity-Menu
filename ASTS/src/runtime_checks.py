# Filename: runtime_integrity_check.py

import hashlib
import logging
from src.utilities import secure_api_request, load_config

logger = logging.getLogger(__name__)

def runtime_integrity_check():
    """
    Perform a run-time integrity check on specified files by verifying their hashes.
    """
    try:
        config = load_config()
        for file_path in config['integrity_check_files']:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            response = secure_api_request("verify-file", {"file_path": file_path, "hash": file_hash})
            if not response or response.get("status") != "ok":
                logger.error("Run-time integrity check failed for %s", file_path)
                raise Exception("Run-time integrity check failed")
        logger.info("Run-time integrity check passed")
    except Exception as e:
        logger.error("Error in run-time integrity check: %s", e)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    runtime_integrity_check()
