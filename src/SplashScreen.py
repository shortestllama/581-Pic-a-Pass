from PyQt5.QtWidgets import QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

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
