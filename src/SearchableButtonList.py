import sys, time, pytz
from datetime import datetime, timezone #to fix the time output
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import AddPasswordProfile
class AddPasswordProfiles( QWidget ):
    def __init__( self ):
        super().__init__()
        #Pull up password profile screen
        self.setWindowTitle( "Create Password Profile" ) #set window title
        self.resize( 900, 600 ) #standard size
        widg = AddPasswordProfile.create() #create widget to create a new password profile
        layout = QVBoxLayout() #create layout for this widget
        layout.addWidget( widg ) #add the password profile class oto the layout
        self.setLayout( layout ) #set the layout to this widget
        self.show() #show this window
class PasswordPofile( QWidget ):
    def __init__(self, label):
        super().__init__()
        self.initUI(label)

    def initUI(self, label):
        self.setWindowTitle("Password Profile")
        self.resize(900, 600)
        
        # Display label in new window
        layout = QVBoxLayout()
        labels = [ "Website", "Username", "Password", "Notes", "Last Updated" ]
        c = 0
        for item in label[:-1]: #get all but the last one (as need to format it)
            label_top = QLabel( f"{labels[ c ]}" )
            label_top.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 24px;
            }
             """)
            c = c + 1  #counter for Labels
            layout.addWidget( label_top )
            label_widget = QLabel(f"{item}")
            label_widget.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 20px;
                border: 1px solid black;
                background-color: white;
            }
             """)
            label_widget.setTextInteractionFlags( Qt.TextSelectableByMouse ) #set selectable flag
            layout.addWidget(label_widget)
        #Fix time
        label_top = QLabel( f"{labels[ c ]}" )
        label_top.setStyleSheet("""
        QLabel {
            font-family: Arial;
            font-size: 24px;
        }
         """)
        layout.addWidget( label_top )
        utc_time = datetime.fromtimestamp( float( label[ 4 ] ), tz=timezone.utc) #fix time
        central_tz = pytz.timezone('America/Chicago') #convert to central time (Best time)
        central_now = utc_time.astimezone(central_tz)
        label_widget = QLabel(f"{central_now.strftime("%m-%d-%Y %H:%M")}")
        label_widget.setStyleSheet("""
        QLabel {
            font-family: Arial;
            font-size: 20px;
            border: 1px solid black;
            background-color: white;
        }
         """)
        label_widget.setTextInteractionFlags( Qt.TextSelectableByMouse ) #set selectable flag
        layout.addWidget(label_widget)
        #Add "Edit Password Profile" button to the bottom
        edit_pw_layout = QHBoxLayout() #create a new layout on the bottom to right justify the add button.
        edit_pw_layout.addStretch() #sets left area of horz to empty to push the button to right justify
        self.edit_pw = QPushButton( "Edit Password Profile", self )
        self.edit_pw.setVisible( True ) #display 
        self.edit_pw.resize( 250, 150 ) #change size
        self.edit_pw.setFont(QFont("Arial", 16))  # Set font size to 16
        edit_pw_layout.addWidget( self.edit_pw ) #add button to right side of horz layout
        layout.addLayout( edit_pw_layout ) #add button to bottom of vertical layout
        self.setLayout(layout)
        self.show()

class SearchableButtonList(QWidget):
    def __init__(self, button_labels):
        super().__init__()
        self.initUI(button_labels)

    def initUI(self, button_labels):
        # Layout setup
        main_layout = QVBoxLayout(self)
        
        # Search bar setup
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_buttons)
        self.search_bar.setFont(QFont("Arial", 16))  # Set font size to 16
        main_layout.addWidget(self.search_bar)
        
        # Scrollable area setup
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 2px solid black;
                border-radius: 10px; /* Adjust the radius as needed */
                
            }
            QScrollArea > QWidget > QWidget {
                background: White; /* Set the background color of the content area */
                border-radius: 10px;
            }
        """)
        main_layout.addWidget(scroll_area)
        
        # Create buttons
        self.buttons = []
        for label in button_labels: #Labels look like: weburl, username, password, notes, timestamp
            button = QPushButton(label[ 0 ], self)
            button.setVisible(True) #make them display in the scroll area 
            button.clicked.connect(lambda checked, l=label: self.button_clicked(l))  # Connect click event
            button.setFont(QFont("Arial", 16))  # Set font size to 16
            self.buttons.append(button)
            self.scroll_layout.addWidget(button)
        #Add "Add password" button to the bottom
        add_pw_layout = QHBoxLayout() #create a new layout on the bottom to right justify the add button.
        add_pw_layout.addStretch() #sets left area of horz to empty to push the button to right justify
        self.add_pw = QPushButton( "Add Password", self )
        self.add_pw.setVisible( True ) #display 
        self.add_pw.resize( 250, 150 ) #change size
        self.add_pw.setFont(QFont("Arial", 16))  # Set font size to 16
        self.add_pw.clicked.connect(lambda checked, l=label: self.add_password())  # Connect click event add password
        add_pw_layout.addWidget( self.add_pw ) #add button to right side of horz layout
        main_layout.addLayout( add_pw_layout ) #add button to bottom of vertical layout
        

    def filter_buttons(self):
        search_text = self.search_bar.text().lower()
        for button in self.buttons:
            button.setVisible(search_text in button.text().lower())
    def button_clicked(self, label): #Control what happens when buttons are clicked.  Open up password profile display screen
        #label is all of the information
        #Labels look like: weburl, username, password, notes, timestamp
        # Open a new window with the password profile
        self.button_window = PasswordPofile(label)
    def add_password( self ):
        self.add_password_window = AddPasswordProfiles()