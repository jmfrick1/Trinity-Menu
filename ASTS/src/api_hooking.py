# Filename: api_hooking.py

import ctypes
import ctypes.wintypes as wintypes
import logging

logger = logging.getLogger(__name__)

WH_CALLWNDPROC = 4
WH_CALLWNDPROCRET = 12

class CWPSTRUCT(ctypes.Structure):
    _fields_ = [
        ("lParam", ctypes.c_int),
        ("wParam", ctypes.c_int),
        ("message", ctypes.c_uint),
        ("hwnd", ctypes.wintypes.HWND)
    ]

HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
original_hook = None

def hook_proc(nCode, wParam, lParam):
    if nCode == 0:  # HC_ACTION
        msg = ctypes.cast(lParam, ctypes.POINTER(CWPSTRUCT)).contents
        if msg.message == wintypes.WM_CLOSE:
            logger.info(f"Intercepted WM_CLOSE message for window {msg.hwnd}")
            # Example: prevent the window from closing
            return 1  # Non-zero to prevent the message from being processed
    return ctypes.windll.user32.CallNextHookEx(original_hook, nCode, wParam, lParam)

def hook_api(api_name, hook_function):
    try:
        global original_hook
        original_hook = ctypes.windll.user32.SetWindowsHookExA(WH_CALLWNDPROC, HOOKPROC(hook_function), None, 0)
        if not original_hook:
            raise ctypes.WinError()
        logger.info(f"Successfully hooked API: {api_name}")
    except Exception as e:
        logger.error(f"Failed to hook API: {api_name} - {e}")
        raise

def unhook_api(api_name):
    try:
        if not ctypes.windll.user32.UnhookWindowsHookEx(original_hook):
            raise ctypes.WinError()
        logger.info(f"Successfully unhooked API: {api_name}")
    except Exception as e:
        logger.error(f"Failed to unhook API: {api_name} - {e}")
        raise

def example_hook_function(nCode, wParam, lParam):
    return hook_proc(nCode, wParam, lParam)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        hook_api("SetWindowsHookExA", example_hook_function)
        # The following is just a placeholder to keep the script running and intercept messages
        import time
        while True:
            time.sleep(1)
        unhook_api("SetWindowsHookExA")
    except Exception as e:
        logger.error(f"Error in API hooking example: {e}")
