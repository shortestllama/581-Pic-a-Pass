from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
# Signup Screen class
#USE QDialog as it blocks creation of other windows until it has finished executing
class SignupScreen(QDialog):
    def __init__(self, my_hash, my_cipher):
        super().__init__()
        self.my_hash = my_hash
        self.my_cipher = my_cipher
        self.setWindowTitle("Sign Up")
        self.setFixedSize(300, 200)


        # Layout setup
        layout = QVBoxLayout()

        # Password input
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password")
        layout.addWidget(self.password_input)

        # Password confirmation input
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm password")
        layout.addWidget(self.confirm_password_input)

        # Signup button
        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.clicked.connect(self.signup)
        layout.addWidget(self.signup_button)

        # Status label for feedback
        self.status_label = QLabel("", self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def signup(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        #TODO
        # add functionality to make sure the password follows NIST standards
        if password != confirm_password:
            self.status_label.setText("Passwords do not match.")
            return

        if not password:
            self.status_label.setText("Password cannot be empty.")
            return

        # Hash the password
        try:
            self.my_hash.gen_hash(password)
            self.my_cipher.gen_key(password)
            self.status_label.setText("Sign-up successful!")
            self.accept() #close this screen and return true

        except Exception as e:
            self.status_label.setText("Error saving password: {e}.")

# Signup Screen class
