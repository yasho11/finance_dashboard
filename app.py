from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QFrame
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from ui.dashboard_view import DashboardView
from ui.import_view import ImportView
from ui.reports_view import ReportsView
from ui.settings_view import SettingsView
from ui.budget_tracker_view import BudgetTrackerView
from ui.expense_prediction_view import ExpensePredictionView  # Import the new view for expense prediction
import sys

class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Dashboard")
        self.setGeometry(300, 100, 1200, 800)
        self.setStyleSheet("""
            background-color: #F1F1F1;
            color: #202020;
            font-family: Arial, sans-serif;
        """)

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Sidebar layout
        sidebar_layout = QVBoxLayout()

        # Sidebar frame with shadow effect
        sidebar_frame = QFrame()
        sidebar_frame.setStyleSheet("""
            background-color: #F1F1F1;
            border-right: 1px solid #A5D8DD;
            padding: 10px;
        """)
        sidebar_frame.setFixedWidth(220)

        # Add buttons to the sidebar
        dashboard_button = self.create_sidebar_button("Dashboard", "icons/dashboard.png")
        import_button = self.create_sidebar_button("Import Data", "icons/import.png")
        reports_button = self.create_sidebar_button("Reports", "icons/report.png")
        settings_button = self.create_sidebar_button("Settings", "icons/settings.png")
        budget_button = self.create_sidebar_button("Budget Tracker", "icons/budget.png")
        predict_button = self.create_sidebar_button("Expense Prediction", "icons/predict.png")  # New button for prediction

        # Connect sidebar buttons to view change
        dashboard_button.clicked.connect(self.show_dashboard)
        import_button.clicked.connect(self.show_import)
        reports_button.clicked.connect(self.show_reports)
        settings_button.clicked.connect(self.show_settings)
        budget_button.clicked.connect(self.show_budget_tracker)
        predict_button.clicked.connect(self.show_expense_prediction)  # Navigate to expense prediction

        # Add buttons to sidebar layout
        for button in [dashboard_button, import_button, reports_button, settings_button, budget_button, predict_button]:
            sidebar_layout.addWidget(button)
        sidebar_layout.addStretch()  # Push everything to the top

        sidebar_frame.setLayout(sidebar_layout)

        # Create stacked widget to switch between views
        self.stacked_widget = QStackedWidget()

        # Add the different views to the stacked widget
        self.stacked_widget.addWidget(DashboardView())  # Index 0: Dashboard
        self.stacked_widget.addWidget(ImportView())     # Index 1: Import Data
        self.stacked_widget.addWidget(ReportsView())    # Index 2: Reports
        self.stacked_widget.addWidget(SettingsView())   # Index 3: Settings
        self.stacked_widget.addWidget(BudgetTrackerView())  # Index 4: Budget Tracker
        self.stacked_widget.addWidget(ExpensePredictionView())  # Index 5: Expense Prediction

        # Add sidebar and stacked widget to the main layout
        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_sidebar_button(self, text, icon_path):
        """Create a styled sidebar button with an icon."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(30, 30))
        button.setFixedHeight(50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #0091D5;
                color: white;
                border-radius: 10px;
                text-align: left;
                padding-left: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #A5D8DD;
            }
        """)
        return button

    # Sidebar button actions to switch views
    def show_dashboard(self):
        """Display the Dashboard view."""
        self.stacked_widget.setCurrentIndex(0)

    def show_import(self):
        """Display the Import Data view."""
        self.stacked_widget.setCurrentIndex(1)

    def show_reports(self):
        """Display the Reports view."""
        self.stacked_widget.setCurrentIndex(2)

    def show_settings(self):
        """Display the Settings view."""
        self.stacked_widget.setCurrentIndex(3)

    def show_budget_tracker(self):
        """Display the Budget Tracker view."""
        self.stacked_widget.setCurrentIndex(4)

    def show_expense_prediction(self):
        """Display the Expense Prediction view."""
        self.stacked_widget.setCurrentIndex(5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
