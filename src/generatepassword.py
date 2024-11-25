import secrets 
import string
from password_strength import SPECIAL_CHARS, p_strength 

class PasswordGenerator:
    def __init__(self, length=18, use_upper=True, use_lower=True, use_digits=True, use_specials=True):
        '''
        Initialize the generator 

        Parameters:
        - length (int): Length of the password
        - use_upper (bool): Include uppercase characters
        - use_lower (bool): Include lowercase characters
        - use_digits (bool): Include digits
        - use_specials (bool): Include special characters

        - Constant Parameters:
        - MIN_LOWERCASE (int): Min Number of lowercase to include in final password
        - MIN_UPPERCASE(int): Min Number of uppercase to include in final password
        - MIN_DIGITS(int): Min Number of numbers to include in final password
        - MIN_SPECIAL(int): Min Number of special characters to include in final password
        - MIN_ENTROPY(float): Min entropy value that a password can have
        '''
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_specials = use_specials
        self.MIN_LOWERCASE = 2
        self.MIN_UPPERCASE = 2
        self.MIN_DIGITS = 2
        self.MIN_SPECIAL = 2
        self.MIN_ENTROPY = 100.0
    

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
           chars += SPECIAL_CHARS
        if not chars:
            raise ValueError("No characters available for genereration.")

        # While true loop until a good password is generated
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(self.length))
            
            # Only check conditions for enabled character types
            meets_requirements = True
            
            # Will go through the password and see if it meets requirements according to specifications
            if self.use_lower:
                lower_count = sum(c.islower() for c in password)
                meets_requirements &= lower_count >= self.MIN_LOWERCASE
                
            if self.use_upper:
                upper_count = sum(c.isupper() for c in password)
                meets_requirements &= upper_count >= self.MIN_UPPERCASE
                
            if self.use_digits:
                digit_count = sum(c.isdigit() for c in password)
                meets_requirements &= digit_count >= self.MIN_DIGITS
                
            if self.use_specials:
                special_count = sum(c in SPECIAL_CHARS for c in password)
                meets_requirements &= special_count >= self.MIN_SPECIAL
                
            if meets_requirements and p_strength(password) >= self.MIN_ENTROPY:
                return password
