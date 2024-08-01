# Your maintenance script here
import logging
import os
import shutil
import subprocess
import sys

logger = logging.getLogger(__name__)

def clean_logs(logs_directory):
    if os.path.exists(logs_directory):
        shutil.rmtree(logs_directory)
        logger.info(f"Logs directory '{logs_directory}' has been cleaned.")
    else:
        logger.warning(f"Logs directory '{logs_directory}' does not exist.")

def backup_database(database_path, backup_path):
    if os.path.exists(database_path):
        shutil.copy2(database_path, backup_path)
        logger.info(f"Database '{database_path}' has been backed up to '{backup_path}'.")
    else:
        logger.warning(f"Database '{database_path}' does not exist.")

def update_dependencies():
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
        logger.info("Dependencies have been updated successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to update dependencies: {e}")

def perform_maintenance():
    logs_directory = "logs"
    database_path = "src/db.sqlite"
    backup_path = "backups/db_backup.sqlite"

    clean_logs(logs_directory)
    backup_database(database_path, backup_path)
    update_dependencies()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    perform_maintenance()
