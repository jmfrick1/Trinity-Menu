# Filename: system_monitoring.py

import psutil
import logging
import time

logger = logging.getLogger(__name__)

def monitor_system(interval=5):
    """
    Monitors system performance metrics and logs them at the specified interval.
    """
    while True:
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        logger.info(f"CPU Usage: {cpu_usage}%")

        # Memory usage
        memory_info = psutil.virtual_memory()
        logger.info(f"Memory Usage: {memory_info.percent}%")
        logger.info(f"Available Memory: {memory_info.available / (1024 * 1024)} MB")

        # Disk usage
        disk_usage = psutil.disk_usage('/')
        logger.info(f"Disk Usage: {disk_usage.percent}%")
        logger.info(f"Free Disk Space: {disk_usage.free / (1024 * 1024 * 1024)} GB")

        # Network stats
        network_info = psutil.net_io_counters()
        logger.info(f"Bytes Sent: {network_info.bytes_sent / (1024 * 1024)} MB")
        logger.info(f"Bytes Received: {network_info.bytes_recv / (1024 * 1024)} MB")

        time.sleep(interval - 1)  # Subtract the interval time already spent

if __name__ == "__main__":
    # Configure logging to print to the console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Start monitoring
    monitor_system(interval=5)
