from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Reports")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #7289da;")
        layout.addWidget(title_label)

        # Placeholder for report data
        report_label = QLabel("No reports available yet.")
        report_label.setAlignment(Qt.AlignCenter)
        report_label.setFont(QFont("Arial", 16))
        layout.addWidget(report_label)

        self.setLayout(layout)
