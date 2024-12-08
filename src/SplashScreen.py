'''
Artifact: Pic-a-Pass SplashScreen.py
Description: Splash screen window for startup
Author(s): Jesse DeBok
Precondition(s): None
Postcondition(s): Main Window is created
Error(s): None
Side effect(s): None
Invariant(s): None
Known fault(s): None

#########################################################################################
| Author       |  Date      | Revise Description                                        |
#########################################################################################
| Jesse DeBok  | 11/07/24   | Document created                                          |
#########################################################################################
'''
from PyQt5.QtWidgets import QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("Pic-a-Pass_logo.png")  #our logo image
        self.setPixmap(pixmap) #set its creation

        # Text on the bottom
        label = QLabel("Loading...", self)
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignCenter) #location in bar
        label.setGeometry(0, pixmap.height() - 30, pixmap.width(), 30)
