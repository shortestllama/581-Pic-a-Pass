import string
import math

# The set of special characters for use in the program
SPECIAL_CHARS = "!@#$%^&*()-_=+<>?{}[]"

def calculate_entropy(password: str) -> float:
    # Calculate password entropy in bits
    char_set_size = 0
    if any(c.isupper() for c in password):
        char_set_size += len(string.ascii_uppercase)
    if any(c.islower() for c in password):
        char_set_size += len(string.ascii_lowercase)
    if any(c.isdigit() for c in password):
        char_set_size += len(string.digits)
    if any(c in SPECIAL_CHARS for c in password):
        char_set_size += len(SPECIAL_CHARS)
        
    return len(password) * math.log2(char_set_size)
