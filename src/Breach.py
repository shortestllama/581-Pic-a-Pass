import hashlib
import requests
import csv
from PyQt5.QtWidgets import (QWidget, QFormLayout, QLabel, 
                          QVBoxLayout, QScrollArea, QPushButton)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import os

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

# Class for the worker thread to check passwords async
class PasswordCheckerThread(QThread):
    result = pyqtSignal(str, str, int)  # Breach found signal
    error = pyqtSignal(str) # Error signal
    finished = pyqtSignal() # Finished signal

    # Constructor that takes in the APIchecker, list of passwords, and the cipher
    def __init__(self, checker, passwords, cipher):
        super().__init__()
        self.checker = checker
        self.passwords = passwords
        self.cipher = cipher

    # Run checks
    def run(self):
        # This indicates some sort of error has happened when parsing csv
        for i, row in enumerate(self.passwords):
            try:
                # Expect: website, username, password, notes, last_updated
                if len(row) < 3:
                    self.error.emit(f"Row {i+1} has insufficient data")
                    continue
                    
                # Grab the website, username, and encrypted password
                website = row[0]
                username = row[1]
                encrypted_password = row[2]

                # Decrypt using the same pattern as password page
                try:
                    decrypted_password = self.cipher.decrypt(
                        encrypted_password, 
                        row[5], 
                        username.encode('utf-8')
                    )
                except Exception as e:
                    self.error.emit(f"Failed to decrypt password for {website}/{username}: {str(e)}")
                    continue

                # Get the number of breaches
                num_breaches = self.checker.check_password(decrypted_password)

                # If a breach has been found, emit the result signal
                if num_breaches > 0:
                    self.result.emit(website, username, num_breaches)
            # If there was an error, emit the signal as an error
            except ConnectionError as e:
                self.error.emit(f"Error checking {website}/{username}: {str(e)}")
            except Exception as e:
                self.error.emit(f"Error processing row {i+1}: {str(e)}")
            
        # Emit the finished signal once finished checking
        self.finished.emit()

def create_breach_page(main_window, cipher) -> QWidget:
    # Initialize the API checker and the UI
    checker = APIChecker()
    breach_page = QWidget(main_window)
    breach_page.setObjectName("breach")
    
    # Create main layout
    main_layout = QVBoxLayout()
    breach_page.setLayout(main_layout)
    
    # Create scroll area for results
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll_content = QWidget()
    results_layout = QFormLayout()
    scroll_content.setLayout(results_layout)
    scroll.setWidget(scroll_content)
    
    # Add header label
    header = QLabel("Password Breach Check Results")
    header.setObjectName("header")
    header.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(header)
    
    # Add scroll area
    main_layout.addWidget(scroll)
    
    # Add check button
    check_button = QPushButton("Check Passwords")
    main_layout.addWidget(check_button)
    
    # Function to start checking
    def start_check():
        # Clear previous results
        for i in reversed(range(results_layout.rowCount())):
            results_layout.removeRow(i)
            
        try:
            # Try to read password file
            if not os.path.exists('passwords.csv'):
                error_label = QLabel("Error: passwords.csv not found!") # If the passwords file isnt there tell the user
                error_label.setStyleSheet("""
                    font-size: 16px;
                """)
                results_layout.addRow(error_label) # Add the error message to the screen
                return
                
            with open('passwords.csv', 'r') as file: # Open the passwords file
                passwords = list(csv.reader(file))
            
            if not passwords: # If the passwords file doesnt exist,
                results_layout.addRow(QLabel("No passwords found in file!")) # Tell the user the file cant be found
                results_layout.setStyleSheet("""
                    font-size: 16px;
                """)
                return
                
            # Disable button
            check_button.setEnabled(False)
            
            # Create and start worker thread
            thread = PasswordCheckerThread(checker, passwords, cipher)
            
            # Function for the result of the worker thread
            def on_result(website, username, num_breaches):
                # Print the website and how many times that password has been breached
                label = QLabel(f"Password for {website} ({username}) has been breached {num_breaches} times!")
                label.setStyleSheet("""
                    font-size: 16px;
                """)
                results_layout.addRow(label) # Add the result to the screen
                
            # Function for error sent from worker thread
            def on_error(error_msg):
                label = QLabel(error_msg) # Print the error message
                label.setStyleSheet("""
                    font-size: 16px;
                """)
                results_layout.addRow(label) # Add it to the screen
                
            # Function for when the worker thread is finished
            def on_finished():
                check_button.setEnabled(True) #Re enable the check passwords button
                if results_layout.rowCount() == 0: #If no breaches were found
                    label = QLabel("No breached passwords found!") # Tell the user no breaches were found
                    label.setStyleSheet("""
                        font-size: 16px;
                    """)
                    results_layout.addRow(label) # Add the message to the screen
            
            # Keep a reference to the thread to prevent garbage collection
            breach_page.thread = thread
                
            # Connect the signal sent from the worker thread to the main one
            thread.result.connect(on_result)
            thread.error.connect(on_error)
            thread.finished.connect(on_finished)

            # Start the worker thread
            thread.start()
                
        # This notifies the user that an error occured when opening password file
        except Exception as e:
            error_label = QLabel(f"Error reading password file: {str(e)}")
            error_label.setStyleSheet("""
                font-size: 16px;
            """)
            results_layout.addRow(error_label)
    
    # Connects the button to the start_check function
    check_button.clicked.connect(start_check)
    return breach_page # Return the breach page for adding to the main window
