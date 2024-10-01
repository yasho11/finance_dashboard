from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QFrame, QFileDialog
)
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QScrollArea
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the expense data to an empty DataFrame to avoid errors
        self.expense_data = pd.DataFrame()

        # Main layout for the entire view
        main_layout = QVBoxLayout(self)

        # Scroll area that will contain the dashboard content
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Scrollable content container
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)  # Add margins for better padding
        scroll_layout.setSpacing(15)  # Spacing between elements

        # Header
        scroll_layout.addLayout(self.create_header())

        # KPI Cards (Top Row)
        scroll_layout.addLayout(self.create_kpi_cards())

        # Button to load CSV data with modern styling
        self.upload_button = QPushButton("Upload File")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                margin: 20px 0;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.upload_button.clicked.connect(self.load_data)
        scroll_layout.addWidget(self.upload_button)

        # Charts Section
        self.charts_layout = self.create_charts_section()
        scroll_layout.addLayout(self.charts_layout)

        # Set scroll area content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def load_data(self):
        """Load data from an Excel file and prepare it for visualization."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Excel File", "", "Excel Files (*.xlsx)")
        if file_path:
            try:
                self.expense_data = pd.read_excel(file_path)
                # Ensure the 'Date' column is in datetime format
                self.expense_data['Date'] = pd.to_datetime(self.expense_data['Date'])

                # Update KPI and charts with the new data
                self.update_kpi_cards()
                self.update_charts()
            except Exception as e:
                print(f"Error loading file: {e}")

    def create_header(self):
        """Creates the header layout with title, website selector, and time periods."""
        header_layout = QHBoxLayout()

        # Title
        title_label = QLabel("Expense Analytics")
        title_label.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold;")
        header_layout.addWidget(title_label)

        return header_layout

    def create_kpi_cards(self):
        """Creates the KPI cards like 'Total Expenses', 'Categories', 'Top Category'."""
        self.kpi_layout = QHBoxLayout()

        # Placeholder KPIs
        kpi_data = [
            {"title": "Total Expenses", "value": "$0", "change": "0%"},
            {"title": "Total Categories", "value": "0", "change": ""},
            {"title": "Top Category", "value": "None", "change": ""}
        ]

        # Create KPI cards
        self.kpi_cards = []
        for kpi in kpi_data:
            card = self.create_kpi_card(kpi["title"], kpi["value"], kpi["change"])
            self.kpi_cards.append(card)
            self.kpi_layout.addWidget(card)

        return self.kpi_layout

    def create_kpi_card(self, title, value, change):
        """Creates a single KPI card with title, value, and percentage change."""
        card = QFrame()
        card.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #dfe6e9;
            border-radius: 10px;
            padding: 10px;
        """)
        card_layout = QVBoxLayout()

        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #2c3e50; font-weight: bold; font-size: 14px;")
        card_layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 22px; color: #2980b9; font-weight: bold;")
        card_layout.addWidget(value_label)

        # Change Percentage (if applicable)
        change_label = QLabel(change)
        change_label.setStyleSheet("font-size: 12px; color: #27ae60;")
        card_layout.addWidget(change_label)

        card.setLayout(card_layout)
        return card

    def update_kpi_cards(self):
        """Updates the KPI cards based on the loaded data."""
        if not self.expense_data.empty:
            total_expenses = self.expense_data['Amount'].sum()
            total_categories = self.expense_data['Category'].nunique()
            top_category = self.expense_data.groupby('Category')['Amount'].sum().idxmax()

            self.kpi_cards[0].layout().itemAt(1).widget().setText(f"${total_expenses:,.2f}")
            self.kpi_cards[1].layout().itemAt(1).widget().setText(f"{total_categories}")
            self.kpi_cards[2].layout().itemAt(1).widget().setText(f"{top_category}")

    def create_charts_section(self):
        """Creates the section with the charts (bar, line, and donut charts)."""
        charts_layout = QVBoxLayout()

        # First Row: Bar chart and Pie/Donut chart
        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.addWidget(self.create_bar_chart())
        self.row_1_layout.addWidget(self.create_donut_chart())
        charts_layout.addLayout(self.row_1_layout)

        # Second Row: Line chart
        self.line_chart = self.create_line_chart()
        charts_layout.addWidget(self.line_chart)

        return charts_layout

    def update_charts(self):
        """Updates the charts with the loaded expense data."""
        # Remove bar chart if it exists
        if self.row_1_layout.itemAt(0) is not None:
            widget = self.row_1_layout.itemAt(0).widget()
            if widget is not None:
                widget.setParent(None)

        # Remove donut chart if it exists
        if self.row_1_layout.itemAt(1) is not None:
            widget = self.row_1_layout.itemAt(1).widget()
            if widget is not None:
                widget.setParent(None)

        # Add updated bar chart
        self.row_1_layout.addWidget(self.create_bar_chart())
    
        # Add updated donut chart
        self.row_1_layout.addWidget(self.create_donut_chart())

        # Remove and update the line chart similarly
        if self.line_chart is not None:
            self.line_chart.setParent(None)
    
        self.line_chart = self.create_line_chart()
        self.charts_layout.addWidget(self.line_chart)


    def create_bar_chart(self):
        """Creates a bar chart for expenses by category."""
        canvas = FigureCanvas(self.generate_bar_chart())
        return canvas

    def create_line_chart(self):
        """Creates a line chart for expenses over time."""
        canvas = FigureCanvas(self.generate_line_chart())
        return canvas

    def create_donut_chart(self):
        """Creates a donut chart for expenses by category."""
        canvas = FigureCanvas(self.generate_donut_chart())
        return canvas

    def generate_bar_chart(self):
        """Generates a bar chart for expenses by category."""
        fig, ax = plt.subplots(figsize=(6, 4))

        if not self.expense_data.empty:
            categories = self.expense_data.groupby('Category')['Amount'].sum()
            categories.plot(kind='bar', ax=ax, color='#3498db')
            ax.set_ylabel('Amount ($)')
            ax.set_title('Expenses by Category')

        return fig

    def generate_line_chart(self):
        """Generates a line chart for expenses over time."""
        fig, ax = plt.subplots(figsize=(6, 4))

        if not self.expense_data.empty:
            self.expense_data.set_index('Date', inplace=True)
            daily_expenses = self.expense_data.resample('D')['Amount'].sum()
            daily_expenses.plot(kind='line', ax=ax, color='#2980b9', marker='o')
            ax.set_title('Daily Expenses Over Time')
            ax.set_ylabel('Amount ($)')

        return fig

    def generate_donut_chart(self):
        """Generates a donut chart for expenses by category."""
        fig, ax = plt.subplots(figsize=(6, 4))

        if not self.expense_data.empty:
            sizes = self.expense_data.groupby('Category')['Amount'].sum()
            labels = sizes.index
            wedges, _ = ax.pie(sizes, wedgeprops=dict(width=0.4), startangle=90, colors=['#3498db', '#e74c3c', '#95a5a6'])

            ax.set(aspect="equal", title='Expenses by Category')
            ax.legend(wedges, labels, title="Category", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        return fig
