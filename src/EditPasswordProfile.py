import sys
import csv
import time
from generatepassword import PasswordGenerator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont
class EditPasswordProfile(QWidget):
    def __init__(self, super_window, super_object, label, password_profile_window ):
        super().__init__()
        self.initUI( super_window, super_object, label, password_profile_window )

    def initUI( self, super_window, super_object, label, password_profile_window ):
        self.setWindowTitle("Edit Password Profile")
        self.resize(900, 600)
        
        # Display label in new window
        self.layout = QVBoxLayout()
        #website
        self.label_website = QLabel( "Website" )
        # self.label_website.setStyleSheet("""
        #     QLabel {
        #         font-family: Arial;
        #         font-size: 24px;
        #     }
        #         """)
        self.layout.addWidget( self.label_website )
        self.label_websiteReal = QLineEdit( label[ 0 ] ) #set label as website name
        # self.label_websiteReal.setStyleSheet("""
        #     QLineEdit {
        #         font-family: Arial;
        #         font-size: 20px;
        #         border: 1px solid black;
        #         background-color: white;
            # }
            #  """)
        self.label_websiteReal.setReadOnly( True )
        self.layout.addWidget( self.label_websiteReal )
        #Username
        self.label_uname = QLabel( "Username" )
        # self.label_uname.setStyleSheet("""
        #     QLabel {
        #         font-family: Arial;
        #         font-size: 24px;
        #     }
        #         """)
        self.layout.addWidget( self.label_uname )
        self.label_unameReal = QLineEdit( label[ 1 ] ) #set label as user name
        # self.label_unameReal.setStyleSheet("""
        #     QLineEdit {
        #         font-family: Arial;
        #         font-size: 20px;
        #         border: 1px solid black;
        #         background-color: white;
            # }
            #  """)
        self.layout.addWidget( self.label_unameReal )
        #Password
        self.label_pw = QLabel( "Password" )
        # self.label_pw.setStyleSheet("""
        #     QLabel {
        #         font-family: Arial;
        #         font-size: 24px;
        #     }
        #         """)
        self.layout.addWidget( self.label_pw )
        self.label_pwReal = QLineEdit( label[ 2 ] ) #set label as user name
        # self.label_pwReal.setStyleSheet("""
        #     QLineEdit {
        #         font-family: Arial;
        #         font-size: 20px;
        #         border: 1px solid black;
        #         background-color: white;
            # }
            #  """)
        self.layout.addWidget( self.label_pwReal )
        #Notes
        self.label_note = QLabel( "Username" )
        # self.label_note.setStyleSheet("""
        #     QLabel {
        #         font-family: Arial;
        #         font-size: 24px;
        #     }
        #         """)
        self.layout.addWidget( self.label_note )
        self.label_noteReal = QLineEdit( label[ 3 ] ) #set label as user name
        # self.label_noteReal.setStyleSheet("""
        #     QLineEdit {
        #         font-family: Arial;
        #         font-size: 20px;
        #         border: 1px solid black;
        #         background-color: white;
            # }
            #  """)
        self.layout.addWidget( self.label_noteReal )
        #Add "Edit Password Profile" button to the bottom
        # Generate button
        generate_button = QPushButton("Generate Password")
        generate_button.clicked.connect( self.generate_pw )
        self.layout.addWidget( generate_button )
        # Save button
        save_button = QPushButton("Save to CSV")
        save_button.clicked.connect(self.save_to_csv)
        save_button.clicked.connect( super_window.close )
        #refresh the main page
        save_button.clicked.connect( super_object.refresh )
        save_button.clicked.connect( password_profile_window.close ) #close password profile menu to get back to list
        self.layout.addWidget(save_button)
        
        self.setLayout( self.layout)
        #self.show()

    def save_to_csv(self):
        # Get values from input fields
        data = [
            self.label_websiteReal.text(),
            self.label_unameReal.text(),
            self.label_pwReal.text(),
            self.label_noteReal.text(),
            time.time()
        ]
        
        # Open file dialog to choose where to save the CSV
        file_path = "passwords.csv"
        
        #save info from csv file except for my edit one
        lines_to_keep = []
    
        with open(file_path, mode='r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            
            # Iterate over each row in the CSV
            for row in reader:
                # If the value in the specified column does not match, keep the line
                if row[ 0 ] != self.label_websiteReal.text():
                    lines_to_keep.append(row)
        lines_to_keep.append( data ) #save new info
        # Write the lines back to the CSV file
        with open(file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(lines_to_keep)
    def generate_pw( self ):
        pw = PasswordGenerator()
        self.label_pwReal.setText( pw.generate_password() )
