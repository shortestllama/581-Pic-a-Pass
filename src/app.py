import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    QSplashScreen,
    QFormLayout,
    QGridLayout
)
#from encryption_utils import Password

class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West) #set on left side of window

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("Pic-a-Pass_logo.png")  # Replace with your image path
        self.setPixmap(pixmap)

        # Optional: Add text to the splash screen
        label = QLabel("Loading...", self)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, pixmap.height() - 30, pixmap.width(), 30)

class LoginScreen(QWidget):
    def __init__(self, next_window):
        super().__init__()
        self.initUI(next_window)

    def initUI(self, next_window):
        self.next_window = next_window

        # Set up layout
        layout = QVBoxLayout()

        # Title label
        self.label = QLabel('Enter Password')
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

    # TODO
    def check_password(self):
        
        password = self.password_input.text()

        # Read from hashed password file and grab salt/hash

        # Using input, salt, and hash, recompute the hash and check if it is correct
        # p = Password(password)
        # return p.check(hash, salt)
        #IF PASSWORD MATCHES:
        self.label.setText("Login successful")
        self.password_input.clear()
        self.close()
        self.next_window.show()

# Signup Screen class
class SignupScreen(QWidget):
    def __init__(self, next_window):
        super().__init__()
        self.setWindowTitle("Sign Up")
        self.setFixedSize(300, 200)

        self.next_window = next_window

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
        #hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Save the hashed password to a file
        try:
            with open("hashed_password.pap", "w") as file:
                file.write(password) #hashed_password)
            self.status_label.setText("Sign-up successful!")
            self.close()  # Close the signup screen
            self.next_window.show()
        except IOError as e:
            self.status_label.setText("Error saving password.")
            print(f"Error: {e}")

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pic-A-Pass")
        #create central widget, everything is on this
        wid = QWidget( self )
        self.setCentralWidget( wid )
        main_layout = QGridLayout()
        wid.setLayout(main_layout)
        
        #password page
        pw_page = QWidget(self)
        layout = QFormLayout()
        pw_page.setLayout(layout)
        layout.addRow('First Name:', QLineEdit(self))
        layout.addRow('Last Name:', QLineEdit(self))
        layout.addRow('DOB:', QDateEdit(self))
        #breach page
        breach_page = QWidget(self)
        layout = QFormLayout()
        breach_page.setLayout(layout)
        layout.addRow('Phone Number:', QLineEdit(self))
        layout.addRow('Email Address:', QLineEdit(self))
        #Tabs
        w = TabWidget()
        w.setStyleSheet( "QTabBar::tab {width: 100px; height: 200px;}" ); #set stylesheet for tab sizes
        w.addTab( pw_page, "Passwords") #set the widget of this tab to the password page widget
        w.addTab( breach_page, "Breaches") #set the widget of this tab to the breach page widget
        w.resize(900, 600) #width, height
        #add to layout
        main_layout.addWidget( w )
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.

def main():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    # Simulate loading process
    import time
    time.sleep(3)

    window = MainWindow()
    window.resize( 900, 600 )

    # Check if the Hashed Password file exists
    hashedpass_file = Path('hashed_password.pap')
    if hashedpass_file.is_file():

        # Display login screen
        #INITIALIZE THE LOGINSCREEN OUTSIDE THIS IF STATEMENT
        #IF WE DECIDE LATER TO GO FROM SIGNUP TO LOGIN INSTEAD
        #OF SIGNUP TO MAIN
        login = LoginScreen(window)
        login.show()
        splash.finish(login)
    
    # If it is not, ask the user for a password and create the file
    else:    
        
        # Display signup screen
        signup = SignupScreen(window) #CHANGE THIS TO LOGIN IF WE
                                      #MAKE THAT CHANGE
        signup.show()
        splash.finish(signup)
    
    #window = MainWindow()
    #window.resize( 900, 600 ) #width, height
    #window.show()

    sys.exit(app.exec())
    
if __name__ == "__main__":
    main() #call main
