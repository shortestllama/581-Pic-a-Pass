import sys, time, pytz
from datetime import datetime, timezone #to fix the time output
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import AddPasswordProfile
import EditPasswordProfile
import csv #for reading from csv and creating buttons
import OptionsWindow
from password_strength import p_strength #password strength function
from qt_material import apply_stylesheet

class PasswordProfile( QWidget ):
    def __init__(self, label, pw_page, hash, cipher):
        super().__init__()
        self.hash = hash
        self.cipher = cipher
        self.password_visible = False # Init to false because password is initially not visible
        self.initUI(label, pw_page)

    def initUI(self, label, pw_page ):
        self.setWindowTitle("Password Profile")
        self.resize(900, 600)
        
        # Display label in new window
        layout = QVBoxLayout()
        labels = [ "Website", "Username", "Password", "Notes", "Last Updated" ]
        c = 0
        for item in label[:-2]: #get all but the last one (as need to format it)
            if c == 2:
                #password so is special
                label_top = QLabel(labels[ c ])
                c = c + 1  #counter for Labels
                layout.addWidget( label_top )
                self.password_label = QLabel("*" * len(item)) #already decrypted from loading it in
                self.password_label.setTextInteractionFlags( Qt.TextSelectableByMouse ) #set selectable flag
                layout.addWidget(self.password_label) # Add the password label as a widget
                self.password = item # Set the password as the current item

                button_layout = QHBoxLayout() # Create a new button layout that will have the clipboard button and the password visiblity button
                button_layout.setSpacing(5) # Put a little space between buttons
                button_layout.addStretch() # Move buttons to the far right

                # Button add password visibility
                self.toggle_button = QPushButton(self) # Create button
                self.toggle_button.setIcon(QIcon("img/open.png"))  # Use the eye icon for the button
                self.toggle_button.setCheckable(True)  # Makes the button toggleable
                self.toggle_button.setFixedSize(24, 24)  # Adjust size for button
                self.toggle_button.clicked.connect(lambda: self.toggle_password_visibility(self.password)) # On click, change visibility of the password
                button_layout.addWidget(self.toggle_button) # Add new button to the button layout

                # Button to copy password to clipboard
                self.clipboard_button = QPushButton(self) # Create button
                self.clipboard_button.setIcon(QIcon("img/clip.png"))  # Use the eye icon for the button
                self.clipboard_button.setFixedSize(24, 24)  # Adjust size for button
                self.clipboard_button.clicked.connect(lambda: self.copy_to_clipboard(self.password)) # Copy password to clipboard
                button_layout.addWidget(self.clipboard_button) # Add clipboard button to button layout
                
                layout.addLayout(button_layout) # Finally, add the buttons to the layout

                self.strength_label = QLabel( "Password strength: Weak" )
                if p_strength( item ) == 0:
                    #weak
                    self.strength_label.setStyleSheet("color: red;")
                elif p_strength( item ) == 1:
                    self.strength_label.setText("Password strength: Medium")
                    self.strength_label.setStyleSheet("color: orange;")
                else:
                    #strong
                    self.strength_label.setText("Password strength: Strong")
                    self.strength_label.setStyleSheet("color: green;")
                self.strength_label.setFont(QFont("Arial", 14))
                layout.addWidget( self.strength_label )
            else:
                label_top = QLabel(labels[ c ])
                c = c + 1  #counter for Labels
                layout.addWidget( label_top )
                self.label_widget = QLabel(item)
                self.label_widget.setTextInteractionFlags( Qt.TextSelectableByMouse ) #set selectable flag
                layout.addWidget(self.label_widget)
        #Fix time
        label_top = QLabel(labels[ c ]) # Set label to correct label
        layout.addWidget( label_top ) # Add label as widget
        utc_time = datetime.fromtimestamp( float( label[ 4 ] ), tz=timezone.utc) #fix time
        central_tz = pytz.timezone('America/Chicago') #convert to central time (Best time)
        central_now = utc_time.astimezone(central_tz)
        self.label_widget = QLabel(f"{central_now.strftime("%m-%d-%Y %H:%M")}")
        self.label_widget.setTextInteractionFlags( Qt.TextSelectableByMouse ) #set selectable flag
        layout.addWidget(self.label_widget)
        #Add "Edit Password Profile" button to the bottom
        edit_pw_layout = QHBoxLayout() #create a new layout on the bottom to right justify the add button.
        edit_pw_layout.addStretch() #sets left area of horz to empty to push the button to right justify
        self.edit_pw = QPushButton( "Edit Password Profile", self )
        self.edit_pw.setVisible( True ) #display 
        self.edit_pw.resize( 250, 150 ) #change size
        self.edit_pw.setFont(QFont("Arial", 16))  # Set font size to 16
        self.edit_pw.clicked.connect( lambda: self.edit_Password( label, pw_page ) )
        edit_pw_layout.addWidget( self.edit_pw ) #add button to right side of horz layout
        layout.addLayout( edit_pw_layout ) #add button to bottom of vertical layout
        self.setLayout(layout)
        self.show()
    def edit_Password( self, label, pw_page ):
        self.edit_password_window = QWidget( )
        #Pull up password profile screen
        self.edit_password_window.setWindowTitle( "Edit Password Profile" ) #set window title
        self.edit_password_window.resize( 900, 600 ) #standard size
        widg = EditPasswordProfile.EditPasswordProfile( self.edit_password_window, pw_page, label, self, self.hash, self.cipher ) #create widget to create a new password profile
        layout = QVBoxLayout() #create layout for this widget
        layout.addWidget( widg ) #add the password profile class oto the layout
        self.edit_password_window.setLayout( layout ) #set the layout to this widget
        self.edit_password_window.show() #show this window

    # Toggles the given password visibility
    # Given password, prints *'s if not visibile and password otherwise
    def toggle_password_visibility(self, password):
        if self.password_visible: # Check if password is currently visibile
            self.password_label.setText("*" * len(password)) # If so, hide it (set it to *'s)
            self.toggle_button.setIcon(QIcon("img/open.png")) # Update icon of button to reflect change
        else: # Password is currently not visible
            self.password_label.setText(password) # Show the password
            self.toggle_button.setIcon(QIcon("img/closed.png")) # Update icon of button to reflect change
        self.password_visible = not self.password_visible # Change state of variable to reflect change

    # Copies the given text to the user's clipboard'
    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard() # Create a clipboard
        clipboard.setText(text) # Set the text of the clipboard

class SearchableButtonList(QWidget):
    def __init__(self, hash, cipher):
        super().__init__()
        self.hash = hash
        self.cipher = cipher
        self.order = 3 #set default order
        self.initUI()

    def initUI(self):
        # Layout setup
        self.main_layout = QVBoxLayout(self)
        
        # Search bar setup
        search_pw_layout = QHBoxLayout() #search bar then options
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_buttons)
        self.search_bar.setFont(QFont("Arial", 16))  # Set font size to 16
        self.search_bar.setStyleSheet("color: white;") # Set the color and bold text

        search_pw_layout.addWidget( self.search_bar ) #add to top bar
        #options button
        self.options = QPushButton( "Options", self )
        self.options.setVisible( True ) #display
        self.options.setFont(QFont("Arial", 16))  # Set font size to 16

        self.options.clicked.connect(lambda: self.create_options())  # Connect click event add password
        search_pw_layout.addWidget( self.options )
        self.main_layout.addLayout( search_pw_layout )
        
        # Scrollable area setup
        self.scroll_area = QScrollArea(self)
        apply_stylesheet(self.scroll_area, theme='dark_teal.xml')
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget( self.scroll_area )
        self.refresh( )
        #Add "Add password" button to the bottom
        add_pw_layout = QHBoxLayout() #create a new layout on the bottom to right justify the add button.
        add_pw_layout.addStretch() #sets left area of horz to empty to push the button to right justify
        self.add_pw = QPushButton( "Add Password", self )
        self.add_pw.setVisible( True ) #display 
        self.add_pw.resize( 250, 150 ) #change size
        self.add_pw.setFont(QFont("Arial", 16))  # Set font size to 16
        self.add_pw.clicked.connect(lambda: self.add_password())  # Connect click event add password
        add_pw_layout.addWidget( self.add_pw ) #add button to right side of horz layout
        self.main_layout.addLayout( add_pw_layout ) #add button to bottom of vertical layout

    def filter_buttons(self):
        search_text = self.search_bar.text().lower()
        for button in self.buttons:
            button.setVisible(search_text in button.text().lower())
    def button_clicked(self, label): #Control what happens when buttons are clicked.  Open up password profile display screen
        #label is all of the information
        #Labels look like: weburl, username, password, notes, timestamp
        # Open a new window with the password profile
        self.button_window = PasswordProfile(label, self, self.hash, self.cipher) #pass in this window as suber object so it can be refreshed upon editing
    def add_password( self ):
        self.add_password_window = QWidget()
        #Pull up password profile screen
        self.add_password_window.setWindowTitle( "Create Password Profile" ) #set window title
        self.add_password_window.resize( 900, 600 ) #standard size
        widg = AddPasswordProfile.AddPasswordProfile( self.add_password_window, self, self.hash, self.cipher ) #create widget to create a new password profile
        layout = QVBoxLayout() #create layout for this widget
        layout.addWidget( widg ) #add the password profile class oto the layout
        self.add_password_window.setLayout( layout ) #set the layout to this widget
        self.add_password_window.show() #show this window
    def create_options( self ):
        #Options window
        #Pull up password profile screen
        options_dialog = OptionsWindow.OptionsWindow()
        #self.options_window.show()
        result = options_dialog.exec_()  # Open the dialog modally

        if result == QDialog.Accepted:
            if options_dialog.get_selected_option() == "Alphabetical":
                self.order = 1
            elif options_dialog.get_selected_option() == "Reverse Alphabetical":
                self.order = 2
            elif options_dialog.get_selected_option() == "Last Changed":
                self.order = 3
            else:
                self.order = 4
        self.refresh() #reset order for new update
    def refresh( self ):
        #order: 1 = alphabetical, 2 = reverse alphabetical, 3 = newest, 4 = oldest
        #refresh data
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_area.setWidget(scroll_content)
        
        # Create buttons
        self.buttons = []
        with open( 'passwords.csv', 'r' ) as file:
            reader = csv.reader( file )
            data = list( reader )
        if (len(data) > 0):
            if (len(data[0]) > 0): # Don't sort if list is empty
                if self.order == 1:
                    #order alphabetical
                    data.sort( key=lambda x: x[0], reverse=False ) #sort by timestamp
                elif self.order == 2:
                    #reverse alphabetical
                    data.sort( key=lambda x: x[0], reverse=True ) #sort by timestamp
                elif self.order == 3:
                    #newest
                    data.sort( key=lambda x: x[-2], reverse=True ) #sort by timestamp
                else:
                    #oldest
                    data.sort( key=lambda x: x[-2], reverse=False ) #sort by timestamp

        for label in data: #Labels look like: weburl, username, password, notes, timestamp, nonce
            if len(label) > 0:
                button = QPushButton(label[ 0 ], self)
                button.setVisible(True) #make them display in the scroll area 
                label[2] = self.cipher.decrypt(label[2], label[5], label[1].encode('utf-8'))
                button.clicked.connect(lambda checked, l=label: self.button_clicked(l))  # Connect click event
                button.setFont(QFont("Arial", 16))  # Set font size to 16
                self.buttons.append(button)
                self.scroll_layout.addWidget(button)
        self.filter_buttons() #also filter the buttons
