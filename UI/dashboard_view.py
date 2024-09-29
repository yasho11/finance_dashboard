from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Dashboard Overview")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #7289da;")
        layout.addWidget(title_label)

        # Sample data or summary
        summary_label = QLabel("Welcome to the Dashboard! Here’s your financial summary.")
        summary_label.setAlignment(Qt.AlignCenter)
        summary_label.setFont(QFont("Arial", 16))
        layout.addWidget(summary_label)

        self.setLayout(layout)
