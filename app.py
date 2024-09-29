from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QFrame
from UI.dashboard_view import DashboardView
from UI.import_view import ImportView
from UI.reports_view import ReportsView
from UI.settings_view import SettingsView
import sys

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Dashboard")
        self.setGeometry(300, 100, 1000, 700)
        self.setStyleSheet("background-color: #2c2f33; color: #ffffff;")

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Sidebar layout
        sidebar_layout = QVBoxLayout()

        # Sidebar frame
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet("background-color: #23272a;")
        sidebar_frame.setFixedWidth(200)

        # Add buttons to the sidebar
        dashboard_button = QPushButton("Dashboard")
        import_button = QPushButton("Import Data")
        reports_button = QPushButton("Reports")
        settings_button = QPushButton("Settings")

        # Connect sidebar buttons to view change
        dashboard_button.clicked.connect(self.show_dashboard)
        import_button.clicked.connect(self.show_import)
        reports_button.clicked.connect(self.show_reports)
        settings_button.clicked.connect(self.show_settings)

        # Add buttons to sidebar layout
        for button in [dashboard_button, import_button, reports_button, settings_button]:
            button.setStyleSheet("background-color: #7289da; color: white; padding: 10px;")
            sidebar_layout.addWidget(button)

        sidebar_frame.setLayout(sidebar_layout)

        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(DashboardView())
        self.stacked_widget.addWidget(ImportView())
        self.stacked_widget.addWidget(ReportsView())
        self.stacked_widget.addWidget(SettingsView())

        # Add sidebar and stacked widget to the main layout
        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def show_dashboard(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_import(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_reports(self):
        self.stacked_widget.setCurrentIndex(2)

    def show_settings(self):
        self.stacked_widget.setCurrentIndex(3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
