from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QPushButton, QFileDialog, QComboBox
from PySide6.QtCore import Qt
from logic.chart import ChartCanvas
import pandas as pd

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()

        # Placeholder for the expense data
        self.expense_data = pd.DataFrame()

        # Main layout
        layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Expense Reports by Time Period")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; color: #7289da;")
        layout.addWidget(title_label)

        # Dropdown to select time period (month/year)
        self.time_period_selector = QComboBox()
        self.time_period_selector.addItem("Compare by Month")
        self.time_period_selector.addItem("Compare by Year")
        self.time_period_selector.currentIndexChanged.connect(self.update_comparison)
        layout.addWidget(self.time_period_selector)

        # Line chart canvas
        self.line_chart = ChartCanvas(width=6, height=4)
        layout.addWidget(self.line_chart)

        # Bar chart canvas
        self.bar_chart = ChartCanvas(width=6, height=4)
        layout.addWidget(self.bar_chart)

        # Button to load CSV data
        self.load_data_button = QPushButton("Load Expense Data")
        self.load_data_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_data_button)

        self.setLayout(layout)

    def load_data(self):
        """Load data from an Excel file and prepare it for comparison."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                # Load the data from the Excel file
                self.expense_data = pd.read_excel(file_path)

                # Ensure the 'Date' column is in datetime format
                self.expense_data['Date'] = pd.to_datetime(self.expense_data['Date'])

                # Perform the initial comparison by month
                self.compare_by_month()
            except Exception as e:
                print(f"Error loading file: {e}")

    def compare_by_month(self):
        """Compare expenses by month."""
        if not self.expense_data.empty:
            df_by_month = self.expense_data.groupby(self.expense_data['Date'].dt.to_period('M')).agg({
            'Amount': 'sum'
            })
            df_by_month.reset_index(inplace=True)
            df_by_month['Date'] = df_by_month['Date'].astype(str)  # Convert to string for chart
            self.update_charts(df_by_month, 'Date', 'Amount', "Monthly Expenses")

    def compare_by_year(self):
        """Compare expenses by year."""
        if not self.expense_data.empty:
            df_by_year = self.expense_data.groupby(self.expense_data['Date'].dt.to_period('Y')).agg({
                'Amount' : 'sum'
            })
            df_by_year.reset_index(inplace=True)
            df_by_year['Date'] = df_by_year['Date'].astype(str)  # Convert to string for chart
            self.update_charts(df_by_year, 'Date', 'Amount', "Yearly Expenses")

    def update_charts(self, df, x_column, y_column, title):
        """Update line and bar charts based on the comparison data."""
        self.line_chart.plot_line_chart(df, x_column, y_column, f"{title} (Line Chart)")
        self.bar_chart.plot_bar_chart(df, x_column, y_column, f"{title} (Bar Chart)")

    def update_comparison(self):
        """Update the comparison based on the selected time period."""
        if self.time_period_selector.currentIndex() == 0:
            self.compare_by_month()
        else:
            self.compare_by_year()
