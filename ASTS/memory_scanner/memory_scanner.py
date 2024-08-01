import logging
import ctypes
import psutil

logger = logging.getLogger(__name__)

class MemoryScanner:
    def __init__(self, process_name):
        self.process_name = process_name
        self.process_handle = None
        self.pid = self.get_pid_by_name(process_name)
        if self.pid:
            self.process_handle = self.open_process(self.pid)
        else:
            logger.error("Process not found")

    def get_pid_by_name(self, process_name):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                return proc.info['pid']
        logger.error(f"Process {process_name} not found")
        return None

    def open_process(self, pid):
        PROCESS_ALL_ACCESS = 0x1F0FFF
        return ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)

    def read_memory(self, address, size):
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        if not ctypes.windll.kernel32.ReadProcessMemory(self.process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)):
            logger.error("Failed to read memory")
            return None
        return buffer.raw

    def find_signature(self, signature, start_address, end_address):
        address = start_address
        signature_length = len(signature)
        while address < end_address:
            buffer = self.read_memory(address, signature_length)
            if buffer and buffer == signature:
                logger.info(f"Found signature at address: {hex(address)}")
                return address
            address += 1
        logger.error("Signature not found")
        return None

    def scan_entities(self, entity_signature, start_address, end_address):
        entities = []
        signature_length = len(entity_signature)
        address = start_address
        while address < end_address:
            buffer = self.read_memory(address, signature_length)
            if buffer and buffer == entity_signature:
                entities.append(address)
                logger.info(f"Found entity at address: {hex(address)}")
            address += signature_length  # Move to the next block
        return entities

    def close(self):
        if self.process_handle:
            ctypes.windll.kernel32.CloseHandle(self.process_handle)
            self.process_handle = None

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    scanner = MemoryScanner("example_process.exe")
    if scanner.process_handle:
        start_address = 0x100000  # Placeholder start address
        end_address = 0x200000    # Placeholder end address
        entity_signature = b"\x00\x01\x02\x03"  # Placeholder signature
        entities = scanner.scan_entities(entity_signature, start_address, end_address)
        logger.info(f"Found entities: {entities}")
        scanner.close()
