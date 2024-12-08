'''
Artifact: Pic-a-Pass generatepassword.py
Description: Generates a password from given parameters
Author(s): Ben Schulte, Caden Lecluyse
Precondition(s): None
Postcondition(s): None
Error(s): None
Side effect(s): None
Invariant(s): None
Known fault(s): None

############################################################################################
| Author          |  Date      | Revise Description                                        |
############################################################################################
| Ben Schulte     | 10/26/24   | Document created                                          |
| Caden Lecluyse  | 11/11/24   | Added minimum requirements for generated password         |
| Caden Lecluyse  | 11/11/24   | Functionality added to get the entropy of a password      |
| Caden Lecluyse  | 11/13/24   | Moved entropy functions to password_strength.py file      |
| Caden Lecluyse  | 11/24/24   | Changed the function that calculates entropy              |
| Caden Lecluyse  | 11/24/24   | Fixed error for password entropy calculation              |
| Ben Schulte     | 12/8/24    | Added prologue and rest of comments                       |
############################################################################################
'''

import secrets # Used for getting characters for generation
import string # Used for getting uppercase/lowercase letters
from password_strength import SPECIAL_CHARS, calculate_entropy, find_sequential_chars # Used for calculating password strength

# Class that handles password generation
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

        Constant Parameters:
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
    
    
    # From the given parameters in initialization, generates a strong enough password
    def generate_password(self) -> str:
        # Generate the pool of characters the parameters allow
        chars = ""
        if self.use_upper: # Check if we are using uppercase
           chars += string.ascii_uppercase # Add uppercase characters to available characters
        if self.use_lower: # Check if we are using lowercase
           chars += string.ascii_lowercase # Add lowercase characters to available characters
        if self.use_digits: # Check if we are using digits
           chars += string.digits # Add digits to available characters
        if self.use_specials: # Check if we are using special characters
           chars += SPECIAL_CHARS # Add special characters to available characters
        if not chars: # In the case that nothing was selected for character pool
            raise ValueError("No characters available for genereration.") # Error when pool is empty

        # While true loop until a good password is generated
        while True:
            password = ''.join(secrets.choice(chars) for _ in range(self.length)) # Generate a new password
            
            # Only check conditions for enabled character types
            meets_requirements = True
            
            # Will go through the password and see if it meets requirements according to specifications
            if self.use_lower: # Check if we use lower
                lower_count = sum(c.islower() for c in password) # Count lowercase chars
                meets_requirements &= lower_count >= self.MIN_LOWERCASE # If there are not enough lowercase chars the password won't meet the requirements
                
            if self.use_upper: # Check if we use upper
                upper_count = sum(c.isupper() for c in password) # Count uppercase chars
                meets_requirements &= upper_count >= self.MIN_UPPERCASE # If there are not enough uppercase chars the password won't meet the requirements
                
            if self.use_digits: # Check if we use digits
                digit_count = sum(c.isdigit() for c in password) # Count digits
                meets_requirements &= digit_count >= self.MIN_DIGITS # If there are not enough uppercase chars the password won't meet the requirements
                
            if self.use_specials: # Chick if we use specials
                special_count = sum(c in SPECIAL_CHARS for c in password) # Count special characters
                meets_requirements &= special_count >= self.MIN_SPECIAL # If there are not enough uppercase chars the password won't meet the requirements
                
            if meets_requirements and (calculate_entropy(password) * find_sequential_chars(password)) >= self.MIN_ENTROPY: # Check if we meet the requirements AND that the entropy is high enough
                return password # Return password and exit loop because we found a strong enough password
