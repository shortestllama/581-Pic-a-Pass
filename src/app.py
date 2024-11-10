from Breach import create_breach_page
import sys
import csv
from PyQt5.QtWidgets import QMainWindow, QWidget
import TabWidget #from file in directory
import SplashScreen
import SearchableButtonList
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
def create_pw_page( self ):
    #read CSV file
    with open( 'passwords.csv', 'r' ) as file:
        reader = csv.reader( file )
        data = list( reader )
    return SearchableButtonList.SearchableButtonList( data )
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
        pw_page = create_pw_page( self )        
        
        #breach page
        breach_page = create_breach_page(self)

        #Tabs
        w = TabWidget.TabWidget()
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
    #splash = SplashScreen.SplashScreen()
    #splash.show()

    # Simulate loading process
    #import time
    #time.sleep(2)
    window = MainWindow(  )
    window.resize( 900, 600 ) #width, height
    window.show()
    #splash.finish(window)
    
   
    app.exec()
    
if __name__ == "__main__":
    main() #call main
