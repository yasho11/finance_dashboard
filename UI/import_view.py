from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QFileDialog, QWidget
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from logic.file_import import import_excel

class ImportView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # File Import Button
        self.import_button = QPushButton("Import Excel File")
        self.import_button.setFont(QFont("Arial", 14))
        self.import_button.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #99aab5;
            }
        """)
        self.import_button.clicked.connect(self.load_file)
        layout.addWidget(self.import_button)

        # Label to display the data or status
        self.data_label = QLabel("No file loaded.")
        self.data_label.setAlignment(Qt.AlignCenter)
        self.data_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.data_label)

        self.setLayout(layout)

    def load_file(self):
        """Function to load file and display data."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx *.csv)")
        
        if file_path:
            data = import_excel(file_path)
            if data is not None:
                self.data_label.setText(str(data.head()))  # Display the first few rows
            else:
                self.data_label.setText("Error loading file.")
