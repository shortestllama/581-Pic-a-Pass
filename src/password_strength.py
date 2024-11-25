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

def find_sequential_chars(password: str, seq_length: int = 3) -> float:
    """
    Check for and penalize sequential patterns in password.
    Returns a penalty value between 0 and 1, where 1 means no sequences found
    and lower values indicate more/longer sequences.
    """
    # Common sequences to check
    sequences = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        "".join(reversed(string.ascii_lowercase)),
        "".join(reversed(string.ascii_uppercase)),
        "".join(reversed(string.digits)),
        "qwerty" + "yuiop" + "asdfg" + "hjkl" + "zxcvb",  # Keyboard patterns
        "!@#$%^&*()",  # Common special char sequences
        "12345678901",
    ]
    
    penalty = 1.0
    password_lower = password.lower()  # For case-insensitive checks
    
    # Check for sequences of different lengths
    for seq_len in range(seq_length, min(len(password) + 1, 7)):
        for sequence in sequences:
            # Look for sequences in forward direction
            for i in range(len(sequence) - seq_len + 1):
                if sequence[i:i+seq_len].lower() in password_lower:
                    # Longer sequences get higher penalties
                    penalty *= (0.9 ** seq_len)
                    
    return max(0.1, penalty)  # Never reduce entropy by more than 90%

# This function will return a 0, 1, 2 for low, medium, high strength passwords
def p_strength(password: str) -> int:
    password_entropy = calculate_entropy(password) # Get the entropy of the password

    # If the entropy is less than 35, return 0
    if password_entropy < 35:
        return 0

    # Get the final score of the password by multiplying the entropy by the penalty
    final_score = password_entropy * find_sequential_chars(password)

    # Return the strength of the password. 35 = low (0), 60 = medium (1), anything above 60 is high (2)
    if final_score < 35:
        return 0
    elif final_score < 60:
        return 1
    else:
        return 2
