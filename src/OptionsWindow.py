from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sort Options")
        self.setGeometry(100, 100, 300, 150)

        # Create layout
        layout = QVBoxLayout()

        # Add label
        label = QLabel("Select a sort option:")
        layout.addWidget(label)

        # Add dropdown (combo box)
        self.dropdown = QComboBox()
        self.dropdown.addItems(["Alphabetical", "Reverse Alphabetical", "Last Changed", "Oldest"])
        layout.addWidget(self.dropdown)

        # Add confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.on_confirm)
        layout.addWidget(confirm_button)

        # Set layout
        self.setLayout(layout)

    def on_confirm(self):
        """Handle the confirm button click."""
        self.accept()  # Close the dialog and set the result to Accepted

    def get_selected_option(self):
        """Retrieve the currently selected option from the dropdown."""
        return self.dropdown.currentText()
