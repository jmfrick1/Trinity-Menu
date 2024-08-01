import psutil
import logging

logger = logging.getLogger(__name__)

class NetworkMonitor:
    def __init__(self):
        self.connections = []

    def get_connections(self):
        self.connections = psutil.net_connections(kind='inet')
        return self.connections

    def log_connections(self):
        self.get_connections()
        for conn in self.connections:
            if conn.raddr:
                logger.info(f"Local address: {conn.laddr}, Remote address: {conn.raddr}, Status: {conn.status}")
            else:
                logger.info(f"Local address: {conn.laddr}, Status: {conn.status}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monitor = NetworkMonitor()
    monitor.log_connections()
