from Breach import create_breach_page
from cryptoutils import PasswordHash, PasswordCipher 
import sys
import csv
from PyQt5.QtWidgets import QMainWindow, QWidget, QShortcut
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtCore import Qt, QEvent
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
    QFrame,
    QDialog
)
from qt_material import apply_stylesheet

#def create_pw_page( self ):
#    #read CSV file
#    with open( 'passwords.csv', 'r' ) as file:
#        reader = csv.reader( file )
#        data = list( reader )
#    return SearchableButtonList.SearchableButtonList( data )

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

        # Add a shortcut for the Enter key
        shortcut = QShortcut(QKeySequence("Return"), self)
        shortcut.activated.connect(self.submit_button.click)

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
# Signup Screen class
#USE QDialog as it blocks creation of other windows until it has finished executing
class SignupScreen(QDialog):
    def __init__(self, my_hash, my_cipher):
        super().__init__()
        self.my_hash = my_hash
        self.my_cipher = my_cipher
        self.setWindowTitle("Sign Up")
        self.setFixedSize(900, 600)


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
            self.status_label.setText(f"Error saving password: {e}.")

# Signup Screen class
# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self, my_hash, my_cipher):
        super().__init__()
        self.setWindowTitle("Pic-A-Pass")
        #create central widget, everything is on this
        wid = QWidget( self )
        self.setCentralWidget( wid )
        main_layout = QGridLayout()
        wid.setLayout(main_layout)
       

        #password page
        self.pw_page = SearchableButtonList.SearchableButtonList( my_hash, my_cipher )
        apply_stylesheet(self.pw_page, theme='dark_teal.xml')
        self.pw_page.setObjectName("pw")
        
        #breach page
        self.breach_page = create_breach_page(self)
        self.breach_page.setObjectName("breach")

        #Tabs
        self.w = TabWidget.TabWidget()
        apply_stylesheet(self.w, theme='dark_teal.xml')

        self.w.setStyleSheet("""
            background-color: #8F9396;
        """)
        #self.w.setStyleSheet( "QTabBar::tab {width: 100px; height: 200px;}" ); #set stylesheet for tab sizes
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
    # Set up hash and cipher
    hash = PasswordHash()
    cipher = PasswordCipher()
    
    app = QApplication(sys.argv)
    splash = SplashScreen.SplashScreen()
    splash.show()
    apply_stylesheet(app, theme='dark_teal.xml')

    # Check if the Hashed Password file exists
    hashedpass_file = Path(hash.PATH)
    if hashedpass_file.is_file():
        
        # Display login screen
        #INITIALIZE THE LOGINSCREEN OUTSIDE THIS IF STATEMENT
        #IF WE DECIDE LATER TO GO FROM SIGNUP TO LOGIN INSTEAD
        #OF SIGNUP TO MAIN
        login = LoginScreen( hash, cipher )
        splash.finish(login)
        if login.exec_() == QDialog.Accepted: #wait for dialog to close
            window = MainWindow( hash, cipher ) #CREATE main window
            apply_stylesheet(window, theme='dark_teal.xml')
            window.resize( 900, 600 ) #width, height
            window.show()
    
    # If it is not, ask the user for a password and create the file
    else:    
        
        # Display signup screen
        signup = SignupScreen( hash, cipher ) #CHANGE THIS TO LOGIN IF WE
                                      #MAKE THAT CHANGE
        splash.finish(signup)
        if signup.exec_() == QDialog.Accepted: #wait for dialog to close
            window = MainWindow( hash, cipher ) #CREATE main window
            window.resize( 900, 600 ) #width, height
            window.show()

    sys.exit(app.exec())
    #app.exec() 
    
if __name__ == "__main__":
    main() #call main
