import logging
import logging.handlers
from utilities import load_config

def setup_logging(level=logging.DEBUG):
    config = load_config()
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # File handler
    fh = logging.FileHandler('app.log')
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    # Secure log transmission to a remote server
    if 'logging_server' in config:
        sh = logging.handlers.HTTPHandler(
            config['logging_server'],
            '/log',
            method='POST',
        )
        logger.addHandler(sh)
    
    logger.addHandler(ch)
    logger.addHandler(fh)

# Example usage
if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete.")
