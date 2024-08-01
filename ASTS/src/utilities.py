import ctypes
import struct
from cryptography.fernet import Fernet
import json
import psutil
import logging
import os

# Load Fernet key from fernet.json
try:
    with open("fernet.json", "r") as fernet_file:
        fernet_config = json.load(fernet_file)
    
    if "key" not in fernet_config:
        raise ValueError("Key not found in fernet.json")
    
    cipher_suite = Fernet(fernet_config["key"])

except FileNotFoundError:
    print("Error: fernet.json not found.")
    exit(1)
except ValueError as ve:
    print(f"Error: {ve}")
    exit(1)
except Exception as e:
    print(f"Error loading Fernet key: {e}")
    exit(1)

def read_memory(process_handle, address, size):
    """
    Read memory from a process.

    Args:
    - process_handle: Handle to the process obtained using `ctypes.windll.kernel32.OpenProcess`.
    - address: Address in the process's memory to read from.
    - size: Number of bytes to read.

    Returns:
    - Raw bytes read from memory.
    """
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_size_t(0)
    ctypes.windll.kernel32.ReadProcessMemory(process_handle, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytesRead))
    return buffer.raw

def decrypt_data(encrypted_data):
    """
    Decrypt encrypted data using the Fernet cipher suite.

    Args:
    - encrypted_data: Encrypted data to decrypt.

    Returns:
    - Decrypted data as bytes.
    """
    return cipher_suite.decrypt(encrypted_data)

def encrypt_data(data):
    """
    Encrypt data using the Fernet cipher suite.

    Args:
    - data: Data to encrypt.

    Returns:
    - Encrypted data as bytes.
    """
    return cipher_suite.encrypt(data)

def find_pattern(process_handle, pattern, mask, start_address, size):
    """
    Search for a pattern in a process's memory.

    Args:
    - process_handle: Handle to the process obtained using `ctypes.windll.kernel32.OpenProcess`.
    - pattern: Pattern to search for as bytes.
    - mask: Mask specifying which bytes in the pattern to compare ('x' for check, '?' for ignore).
    - start_address: Starting address in the process's memory to begin searching.
    - size: Number of bytes to search.

    Returns:
    - Address where the pattern was found, or None if not found.
    """
    buffer = read_memory(process_handle, start_address, size)
    pattern_length = len(mask)
    for i in range(len(buffer) - pattern_length):
        match = True
        for j in range(pattern_length):
            if mask[j] == 'x' and buffer[i + j] != pattern[j]:
                match = False
                break
        if match:
            return start_address + i
    return None

def hide_process(process_name):
    """
    Hide the window of a process by its name.

    Args:
    - process_name: Name of the process to hide.

    Raises:
    - Exception if the process cannot be found or its handle cannot be obtained.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            PROCESS_VM_READ = 0x0010
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ, False, proc.info['pid'])
            if handle:
                ctypes.windll.user32.ShowWindow(proc.info['pid'], 0)  # 0 = SW_HIDE
                ctypes.windll.kernel32.CloseHandle(handle)
                return
            raise Exception(f"Could not open process: {process_name}")
    raise Exception(f"Process not found: {process_name}")

def get_process_handle(process_name):
    """
    Get the handle of a process by its name.

    Args:
    - process_name: Name of the process to retrieve the handle for.

    Returns:
    - Handle to the process if found.

    Raises:
    - Exception if the process cannot be found or its handle cannot be obtained.
    """
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
            handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, proc.info['pid'])
            if handle:
                return handle
            raise Exception(f"Could not open process: {process_name}")
    raise Exception(f"Process not found: {process_name}")

def get_module_base_address(process_handle, module_name):
    """
    Get the base address of a module in a process.

    Args:
    - process_handle: Handle to the process obtained using `ctypes.windll.kernel32.OpenProcess`.
    - module_name: Name of the module to find.

    Returns:
    - Base address of the module if found, else None.
    """
    hModuleSnap = ctypes.windll.kernel32.CreateToolhelp32Snapshot(0x00000008, 0)
    if hModuleSnap == -1:
        return None
    moduleEntry = ctypes.wintypes.MODULEENTRY32()
    moduleEntry.dwSize = ctypes.sizeof(ctypes.wintypes.MODULEENTRY32)
    success = ctypes.windll.kernel32.Module32First(hModuleSnap, ctypes.byref(moduleEntry))
    while success:
        if moduleEntry.szModule.decode('utf-8') == module_name:
            ctypes.windll.kernel32.CloseHandle(hModuleSnap)
            return moduleEntry.modBaseAddr
        success = ctypes.windll.kernel32.Module32Next(hModuleSnap, ctypes.byref(moduleEntry))
    ctypes.windll.kernel32.CloseHandle(hModuleSnap)
    return None

def get_logger(name):
    """
    Get a logger instance with a specified name.

    Args:
    - name: Name of the logger.

    Returns:
    - Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

def load_config():
    """
    Load configuration from config.json.

    Returns:
    - Config as a dictionary.
    """
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("Error: config.json not found.")
        exit(1)

def is_debug_mode():
    """
    Check if the application is in debug mode.

    Returns:
    - Boolean indicating if debug mode is enabled.
    """
    config = load_config()
    return config.get("debug_mode", False)

def monitor_system():
    """
    Monitor the system for specific events (placeholder function).
    """
    print("Monitoring system...")

def verify_file_integrity(file_path):
    """
    Verify the integrity of a file (placeholder function).

    Args:
    - file_path: Path to the file to verify.
    """
    print(f"Verifying file integrity for {file_path}")

def execute_at_time(time, function, *args):
    """
    Execute a function at a specified time (placeholder function).

    Args:
    - time: Time to execute the function.
    - function: Function to execute.
    - args: Arguments to pass to the function.
    """
    print(f"Executing function at {time}")
