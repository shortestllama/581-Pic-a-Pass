import random
import string

class PasswordGenerator:
    def __init__(self, length=12, use_upper=True, use_lower=True, use_digits=True, use_specials=True):
        '''
        Initialize the generator 

        Parameters:
        - length (int): Length of the password
        - use_upper (bool): Include uppercase characters
        - use_lower (bool): Include lowercase characters
        - use_digits (bool): Include digits
        - use_specials (bool): Include special characters
        '''
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_specials = use_specials

    def generate_password(self) -> str:
        '''
        Generate a password from the given parameters.
        
        Return: The generated password
        '''
        # Generate the pool of characters the parameters allow
        chars = ""
        if self.use_upper:
           chars += string.ascii_uppercase
        if self.use_lower:
           chars += string.ascii_lowercase
        if self.use_digits:
           chars += string.digits
        if self.use_specials:
           chars += "!@#$%^&*()-_=+<>?{}[]"
        if not chars:
            raise ValueError("No characters available for genereration.")

        password = ''.join(random.choice(chars) for _ in range(self.length))
        return password
