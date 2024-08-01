import hashlib
import logging
import os
from utilities import load_config

logger = logging.getLogger(__name__)

def verify_whitelist():
    try:
        config = load_config()
        hwid = get_hwid()
        if hwid not in config['whitelisted_hardware']:
            logger.error("HWID not in whitelist: %s", hwid)
            raise Exception("HWID not in whitelist")
        logger.info("HWID verification passed")
    except Exception as e:
        logger.error("Error in HWID verification: %s", e)

def get_hwid():
    # Generate a unique hardware ID (HWID) based on system components
    hwid_source = f"{os.uname().nodename}{os.uname().machine}{os.uname().version}"
    return hashlib.sha256(hwid_source.encode()).hexdigest()
