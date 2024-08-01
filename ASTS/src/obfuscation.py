# Filename: dynamic_obfuscation.py

import random

def dynamic_obfuscation():
    """
    Dynamically obfuscate function names to prevent detection.
    """
    obfuscated_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
    globals()[obfuscated_name] = some_function
    return obfuscated_name

def some_function():
    """
    A sample function to demonstrate dynamic obfuscation.
    """
    print("This is a dynamically obfuscated function.")

# Example usage
if __name__ == "__main__":
    obfuscated_name = dynamic_obfuscation()
    print(f"Obfuscated function name: {obfuscated_name}")
    globals()[obfuscated_name]()
