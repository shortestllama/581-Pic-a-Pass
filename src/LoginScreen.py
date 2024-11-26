from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton
)
#USE QDialog as it blocks creation of other windows until it has finished executing
class LoginScreen(QDialog):
    def __init__(self, my_hash, my_cipher):
        super().__init__()
        self.setObjectName("login_screen")
        self.my_hash = my_hash
        self.my_cipher = my_cipher
        self.initUI()

    def initUI(self):

        # Set up layout
        layout = QVBoxLayout()

        # Set up picture
        self.pic = QLabel("")
        self.pic.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("gear.png")
        scaled_pixmap = pixmap.scaled(
            150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.pic.setPixmap(scaled_pixmap)
        layout.addWidget(self.pic)

        # Title label
        self.label = QLabel('Enter Password')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        # Password input field
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide password text
        layout.addWidget(self.password_input)

        # Submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.check_password)
        layout.addWidget(self.submit_button)

        # Set the layout
        self.setLayout(layout)

        # Center the window and set title
        self.setWindowTitle("Login Screen")
        self.resize(900, 600)
        self.setFixedSize(self.size())  # Fix size to prevent resizing

    def check_password(self):
        password = self.password_input.text()
        correct = self.my_hash.check_pwd(password)
        if correct:
            self.my_cipher.gen_key(password)
            self.label.setText("Login successful")
            self.password_input.clear()
            self.accept() #close this screen and return true
        else:
            self.label.setText("Password incorrect")
            self.password_input.clear()
