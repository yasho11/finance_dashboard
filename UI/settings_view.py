from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #7289da;")
        layout.addWidget(title_label)

        # Placeholder for settings options
        settings_label = QLabel("Settings will be here.")
        settings_label.setAlignment(Qt.AlignCenter)
        settings_label.setFont(QFont("Arial", 16))
        layout.addWidget(settings_label)

        self.setLayout(layout)
