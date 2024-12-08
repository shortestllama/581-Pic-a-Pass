'''
Artifact: Pic-a-Pass cryptoutils.py
Description: A group of utility functions for the cryptography behind the application
Author(s): Ben Schulte
Precondition(s): None
Postcondition(s): None
Error(s):
- FileExistsError: File exists already when trying to generate hash or key
- FileNotExistsError: File does not exist when trying to read password data
- EmptyHashError: Hash is empty when trying to write hash to file
- EmptyKeyError: Key is empty when trying to encrypt/decrypt
- EmptySaltError: Salt is empty when trying to write salt to file
Side effect(s): Decryption can fail if someone has altered the passwords.csv
Invariant(s): None
Known fault(s): None

#########################################################################################
| Author       |  Date      | Revise Description                                        |
#########################################################################################
| Ben Schulte  | 11/23/24   | Document created                                          |
| Ben Schulte  | 11/24/24   | Updated functions to output base64 encoded data to files  |
| Ben Schulte  | 12/3/24    | Added functions for doing steganography                   |
| Ben Schulte  | 12/8/24    | Added final comments to the document                      |
#########################################################################################
'''

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC # Used for generating symmetric key from password
from cryptography.hazmat.primitives.hashes import SHA256 # Used for hasing
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes # Used for general crypto
from cryptography.hazmat.primitives.ciphers.aead import AESGCM # Algorithm used for encrypting passwords
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction # Needed for PBKDF2HMAC
from pathlib import Path # Used for checking if paths exist
from typing import Tuple # Used for returning tuples
from PIL import Image # Used for handling image files for steg
import stepic # Used for steg functions
import base64 # Used for base64 encoding/decoding
import bcrypt # Used for hashing master password
import os # Used for generating random values

'''
Classes used for error handling
'''
class FileExistsError(Exception): # Handles when a file exists already
    pass
class FileNotExistsError(Exception): # Handles when a file doesn't exist
    pass
class EmptyHashError(Exception): # Handles when you try to check the password when there is no hash
    pass
class EmptyKeyError(Exception): # Handles when you try to encrypt/decrypt without generating key first
    pass
class EmptySaltError(Exception): # Handles when the salt is missing
    pass

'''
Class used for generating and checking the master password hash
'''
class PasswordHash:
    def __init__(self):
        '''
        salt: Salt used in hash function 
        hash: Hash generated from master password
        PATH: Path to datafile
        '''
        self.salt = bcrypt.gensalt() # Generate a salt using bcrypt
        self.hash = None # Init hash as none
        self.TMP_IMG = "img/.tmp.png" # Path used for getting the initial image for steg
        self.PATH = "img/masterpassword.png" # Path used for putting 
       
    # Generate the master password hash. Writes hash and salt to the datafile
    # pwd: The password to use to generate the hash
    def gen_hash(self, pwd: str) -> None:
        # Check if hash already exists
        datafile = Path(self.PATH) # Set path
        if datafile.is_file(): # Check if path exists
            raise FileExistsError ("Hash has already been generated") # Error if path exists
        # Create the new hash using the new salt
        self.hash = bcrypt.hashpw(pwd.encode('utf-8'), self.salt) # Use bcrypt to hash the password
        self.__write_data() # Write password data to file

    # Checks a password and sees if it matches the hash. Reads the data from the datafile
    # pwd: The password to check the hash with
    # @ret: Whether or not the password was correct
    def check_pwd(self, pwd) -> bool:
        self.__read_data() # Read data from file
        return self.hash == bcrypt.hashpw(pwd.encode('utf-8'), self.salt) # Check if the hash of the given password is the same as the one written to the file

    # Writes the hash and salt to a file
    def __write_data(self) -> None:
        if (self.hash is None): # First check if there is a hash generated
            raise EmptyHashError ("No hash has been generated") # Error if it has not been generated

        text = self.salt + b'\t' + self.hash # Create text that will be encoded
        encode_image(self.TMP_IMG, text, self.PATH) # Encode text using the base image and create the steg file

    # Reads the hash and salt from a file
    def __read_data(self) -> None:
        # Check for datafile
        datafile = Path(self.PATH) # Set path
        if not datafile.is_file(): # Check is path exists
            raise FileNotExistsError ("Hash file has not been generated") # If it isn't a file, error

        data = decode_image(self.PATH).split('\t') # Decode data from steg function and parse it
        self.salt, self.hash = data[0].encode('utf-8'), data[1].encode('utf-8') # Set correct values for hash and salt from file

'''
Class used for key generation and password encryption/decryption
'''
class PasswordCipher:
    '''
    salt: Salt used for PBKDF2
    key: Key generated from PBKDF2
    PATH: Path of datafile
    ALG: Algorithm to use for PBKDF2
    KEYLEN: Length of the key generated from PBKDF2
    ITR: Number of iterations to do for PBKDF2
    '''
    def __init__(self):
        self.salt = None
        self.key = None

        self.TMP_IMG = "img/.tmp.png"
        self.PATH = "img/encryptionkey.png"
        self.ALG = SHA256()
        self.KEYLEN = 32
        self.ITR = 100000

    # Use PBKDF2 to generate a key from a given password
    # pwd: The password used to generate the symmetric key
    # @ret: The generated symmetric key
    def gen_key(self, pwd: str) -> bytes:
        datafile = Path(self.PATH) # Grab path
        if datafile.is_file(): # Check if salt has been generated
            self.__read_data() # Grab salt from file
        else: # Salt has not been generated yet
            self.salt = os.urandom(12) # Generate new salt
            self.__write_data() # Write new salt to file

        # Generate KDF using given parameters in init
        kdf = PBKDF2HMAC(
            algorithm=self.ALG,
            length=self.KEYLEN,
            salt=self.salt,
            iterations=self.ITR,
        )
        
        self.key = kdf.derive(pwd.encode('utf-8')) # Use the kdf to generate a key
        return self.key # Return the generated key

    # Encrypt the given plaintext using the generated symmetric key, generated nonce, and authentication data
    # ct: The plaintext to encrypt
    # aad: The authentication data. Use a byte encoded string of data relevant to the password. (e.g. aad=b"gmail.com")
    # @ret: The encrypted password
    def encrypt(self, pt: str, aad: bytes = b"") -> Tuple[bytes, bytes]:
        if (self.key is None): # Check if there is a key for encryption
            raise EmptyKeyError("No key for encryption") # Error if not
        aesgcm = AESGCM(self.key) # Use key to create the cipherj
        nonce = os.urandom(12) # Generate a random number (Nonce)
        ct = base64.b64encode(aesgcm.encrypt(nonce, pt.encode('utf-8'), aad)) # Encrypt with algorithm with generated values and base64 encode it 
        nonce = base64.b64encode(nonce) # base64 encode the nonce
        return ct, nonce # Return the ciphertext and the nonce as a tuple
    
    # Decrypt the given ciphertext using the generated symmetric key, given nonce, and authentication data
    # ct: The ciphertext to decrypt
    # nonce: The nonce used for the algorithm. Use the nonce generated in the encryption of the password
    # aad: The authentication data. Use a byte encoded string of data relevant to the password. (e.g. aad=b"gmail.com")
    # @ret: The decrypted password
    def decrypt(self, ct: bytes, nonce: bytes, aad: bytes = b"") -> str:
        if (self.key is None): # Check if there is a key for decryption
            raise EmptyKeyError("No key for decryption") # Error if there isn't a key
        aesgcm = AESGCM(self.key) # Use key to create a cipher
        try: 
            pt = aesgcm.decrypt(base64.b64decode(nonce), base64.b64decode(ct), aad) # Try decrypting
        except Exception as e: # Catch exception
            return f"Decryption failed: {e}" # Decryption failed due to file being altered
        return pt.decode('utf-8') # Return the decoded password

    # Writes the salt to the PBKDF2 data file
    def __write_data(self) -> None:
        if (self.salt is None): # Check if there is a salt to write
            raise EmptySaltError ("No salt has been generated") # Error if no salt
        encode_image(self.TMP_IMG, base64.b64encode(self.salt), self.PATH) # Encode the salt as an image

    # Reads the salt from the PBKDF2 data file
    def __read_data(self) -> None: 
        datafile = Path(self.PATH) # Get path
        if not datafile.is_file(): # Check if there is a file
            raise FileNotExistsError ("Key file has not been generated") # Error if no file

        self.salt = base64.b64decode(decode_image(self.PATH)) # Grab salt from file after decoding image

'''Steganography functions'''
# Encode text within an image file
def encode_image(image_path, text: bytes, output_path):
    image = Image.open(image_path) # Open the image
    encoded_image = stepic.encode(image, text) # Use stepic to encode the text in the image
    encoded_image.save(output_path) # Save the encoded data to the output file

# Decode given image file
def decode_image(image_path):
    image = Image.open(image_path) # Open the image
    decoded_text = stepic.decode(image) # Use stepic to decode the text in the image
    return decoded_text # Return the text that was found from decoding
