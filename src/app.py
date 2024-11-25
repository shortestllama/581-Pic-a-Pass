from Breach import create_breach_page
from cryptoutils import PasswordHash, PasswordCipher 
import sys
import csv
from PyQt5.QtWidgets import QMainWindow, QWidget
import TabWidget #from file in directory
import SplashScreen
import SearchableButtonList
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication,
    QTableView,
    QLineEdit,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QFrame
)

# Set up hash and cipher
hash = PasswordHash()
cipher = PasswordCipher()

def create_pw_page( self ):
    #read CSV file
    with open( 'passwords.csv', 'r' ) as file:
        reader = csv.reader( file )
        data = list( reader )
    return SearchableButtonList.SearchableButtonList( data )


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

    def check_password(self):
        password = self.password_input.text()
        correct = hash.check_pwd(password)
        if correct:
            cipher.gen_key(password)
            self.label.setText("Login successful")
            self.password_input.clear()
            self.close()
            self.next_window.show()
        else:
            self.label.setText("Password incorrect")
            self.password_input.clear()

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
        try:
            hash.gen_hash(password)
            cipher.gen_key(password)
            self.status_label.setText("Sign-up successful!")
            self.close()  # Close the signup screen
            self.next_window.show()

        except Exception as e:
            self.status_label.setText("Error saving password: {e}.")

# Signup Screen class
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
        self.pw_page = SearchableButtonList.SearchableButtonList( hash, cipher )       
        
        #breach page
        self.breach_page = create_breach_page(self)

        #Tabs
        self.w = TabWidget.TabWidget()
        self.w.setStyleSheet( "QTabBar::tab {width: 100px; height: 200px;}" ); #set stylesheet for tab sizes
        self.w.addTab( self.pw_page, "Passwords") #set the widget of this tab to the password page widget
        self.w.addTab( self.breach_page, "Breaches") #set the widget of this tab to the breach page widget
        self.w.resize(900, 600) #width, height
        self.w.currentChanged.connect( self.on_tab_change )
        #add to layout
        main_layout.addWidget( self.w )
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
    def on_tab_change( self, index ):
        #refresh the tab
        if index == 0:
            #refresh tab 1
            self.pw_page.refresh()
        elif index == 1:
            #refresh tab 2
            #TODO
            print( "TODO" )

def main():
    app = QApplication(sys.argv)
    splash = SplashScreen.SplashScreen()
    splash.show()

    # Simulate loading process
    import time
    time.sleep(3)

    window = MainWindow()
    window.resize( 900, 600 )

    # Check if the Hashed Password file exists
    hashedpass_file = Path(hash.PATH)
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
    #app.exec() 
    
if __name__ == "__main__":
    main() #call main
