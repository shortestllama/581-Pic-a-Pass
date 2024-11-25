import hashlib
import requests
import csv
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import (
    QLabel,
    QFormLayout,
)

class APIChecker:
    # Initialize the checker with the api url
    def __init__(self):
        self.url = "https://api.pwnedpasswords.com/range/"
    
    # The API requires the first 5 characters of a sha1 hash
    def _get_sha1_hash(self, password: str) -> str:
        return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # Query the have i been pwned api
    def _query_api(self, hash_prefix: str) -> str:
        try:
            # Perform a get request with the format: api_url/hash_prefix 
            response = requests.get(f"{self.url}{hash_prefix}")
            if response.status_code != 200:
                raise ConnectionError(f"API returned status code {response.status_code}")
            # Return the response
            return response.text
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to check password: {str(e)}")

    # This will actually check the password
    def check_password(self, password: str) -> int:
        # Generate the hash, and then split it into prefix and suffix
        password_hash = self._get_sha1_hash(password)
        hash_prefix = password_hash[:5]
        hash_suffix = password_hash[5:]

        # Get the api response, if not throw the error it gives
        # Can potentially deal with and catch the error here I'm just not sure what we're doing yet
        try:
            api_response = self._query_api(hash_prefix)
        except ConnectionError as e:
            raise e

        # Check if the suffix exists in the response
        for line in api_response.splitlines():
            suffix, count = line.split(':')
            if suffix == hash_suffix:
                # Return the number of data breaches
                return int(count)

        # Return false iff the suffix isnt in the response
        return 0

# This will create the breach page
def create_breach_page(main_window) -> QWidget:
    # Initialize the api checker and the ui
    checker = APIChecker()
    breach_page = QWidget(main_window)
    breach_page.setObjectName("breach")
    layout = QFormLayout()
    breach_page.setLayout(layout)
    # Open the password file
    with open( 'passwords.csv', 'r' ) as file:
        reader = csv.reader( file )
        # Loop through the entries and check the second entry with the api
        for row in reader:
            if len(row) > 0:
                try:
                    # If the password is in the api response, print the result
                    num_breaches = checker.check_password(row[2])
                    if (num_breaches > 0):
                        layout.addRow(QLabel(f"Password for {row[0]} breached {num_breaches} times!"))
                except ConnectionError as e:
                    layout.addRow(QLabel(f"Error in check_password: {str(e)}"))


    # Return the widget for adding to the main window
    return breach_page
