from Breach import create_breach_page
import sys
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
#Breach page requires requests module
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
        self.pw_page = SearchableButtonList.SearchableButtonList( )       
        
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
