from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf import KeyDerivationFunction
from pathlib import Path
from typing import Tuple
from PIL import Image
import stepic # Used for steg functions
import base64
import bcrypt
import os


'''
Classes used for error handling
'''
class FileExistsError(Exception):
    pass
class FileNotExistsError(Exception):
    pass
class EmptyHashError(Exception):
    pass
class EmptyKeyError(Exception):
    pass
class EmptySaltError(Exception):
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
        self.salt = bcrypt.gensalt()
        self.hash = None
        self.TMP_IMG = "img/.tmp.png"
        self.PATH = "img/masterpassword.png"
       
    # Generate the master password hash. Writes hash and salt to the datafile
    # pwd: The password to use to generate the hash
    def gen_hash(self, pwd: str) -> None:
        # Check if hash already exists
        datafile = Path(self.PATH)
        if datafile.is_file():
            raise FileExistsError ("Hash has already been generated")
        # Create the new hash using the new salt
        self.hash = bcrypt.hashpw(pwd.encode('utf-8'), self.salt)
        self.__write_data()

    # Checks a password and sees if it matches the hash. Reads the data from the datafile
    # pwd: The password to check the hash with
    # @ret: Whether or not the password was correct
    def check_pwd(self, pwd) -> bool:
        self.__read_data()
        return self.hash == bcrypt.hashpw(pwd.encode('utf-8'), self.salt)

    # Writes the hash and salt to a file
    def __write_data(self) -> None:
        if (self.hash is None):
            raise EmptyHashError ("No hash has been generated")

        text = self.salt + b'\t' + self.hash
        encode_image(self.TMP_IMG, text, self.PATH)

    # Reads the hash and salt from a file
    def __read_data(self) -> None:
        # Check for datafile
        datafile = Path(self.PATH)
        if not datafile.is_file():
            raise FileNotExistsError ("Hash file has not been generated")

        data = decode_image(self.PATH).split('\t')
        self.salt, self.hash = data[0].encode('utf-8'), data[1].encode('utf-8')

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
        datafile = Path(self.PATH)
        if datafile.is_file():
            # Grab salt from file
            self.__read_data()
        else:
            # Generate new salt
            self.salt = os.urandom(12)
            self.__write_data()

        # Generate KDF
        kdf = PBKDF2HMAC(
            algorithm=self.ALG,
            length=self.KEYLEN,
            salt=self.salt,
            iterations=self.ITR,
        )
        
        # Generate key from KDF and password
        self.key = kdf.derive(pwd.encode('utf-8'))
        return self.key

    # Encrypt the given plaintext using the generated symmetric key, generated nonce, and authentication data
    # ct: The plaintext to encrypt
    # aad: The authentication data. Use a byte encoded string of data relevant to the password. (e.g. aad=b"gmail.com")
    # @ret: The encrypted password
    def encrypt(self, pt: str, aad: bytes = b"") -> Tuple[bytes, bytes]:
        if (self.key is None):
            raise EmptyKeyError("No key for encryption")
        aesgcm = AESGCM(self.key)
        nonce = os.urandom(12)
        ct = base64.b64encode(aesgcm.encrypt(nonce, pt.encode('utf-8'), aad))
        # aesgcm.decrypt(nonce, base64.b64decode(ct), )
        nonce = base64.b64encode(nonce)
        return ct, nonce
    
    # Decrypt the given ciphertext using the generated symmetric key, given nonce, and authentication data
    # ct: The ciphertext to decrypt
    # nonce: The nonce used for the algorithm. Use the nonce generated in the encryption of the password
    # aad: The authentication data. Use a byte encoded string of data relevant to the password. (e.g. aad=b"gmail.com")
    # @ret: The decrypted password
    def decrypt(self, ct: bytes, nonce: bytes, aad: bytes = b"") -> str:
        if (self.key is None):
            raise EmptyKeyError("No key for decryption")
        aesgcm = AESGCM(self.key)
        try:
            pt = aesgcm.decrypt(base64.b64decode(nonce), base64.b64decode(ct), aad)
        except Exception as e:
            return f"Decryption failed: {e}"
        return pt.decode('utf-8')

    # Writes the salt to the PBKDF2 data file
    def __write_data(self) -> None:
        if (self.salt is None):
            raise EmptySaltError ("No salt has been generated")
        encode_image(self.TMP_IMG, base64.b64encode(self.salt), self.PATH)

    def __read_data(self) -> None:
        datafile = Path(self.PATH)
        if not datafile.is_file():
            raise FileNotExistsError ("Key file has not been generated")

        self.salt = base64.b64decode(decode_image(self.PATH))

'''Steganography functions'''

# Encode text within an image file
def encode_image(image_path, text: bytes, output_path):
    image = Image.open(image_path)
    encoded_image = stepic.encode(image, text)
    encoded_image.save(output_path)

# Decode given image file
def decode_image(image_path):
    image = Image.open(image_path)
    decoded_text = stepic.decode(image)
    return decoded_text
