from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QWidget, QFileDialog, QDateEdit, QScrollArea, QFrame
from PySide6.QtCore import Qt, Signal, QDate
import pandas as pd
from datetime import datetime

class BudgetTrackerView(QWidget):
    # Signal emitted when an expense is added or updated
    budget_updated = Signal(dict)

    def __init__(self):
        super().__init__()

        # Main container for scroll area
        main_layout = QVBoxLayout(self)

        # Scroll area that will contain the budget tracker
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Scrollable content container
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)

        # Sample budget categories and initial amounts
        self.budget_data = {
            'Groceries': {'budget': 500, 'spent': 0},
            'Rent': {'budget': 1000, 'spent': 0},
            'Utilities': {'budget': 200, 'spent': 0}
        }

        # Budget tracking widgets (labels, input fields, progress bars)
        self.budget_widgets = {}
        for category in self.budget_data:
            category_layout = QVBoxLayout()

            # Category label with enhanced styling
            category_label = QLabel(f"{category} Budget")
            category_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")
            category_layout.addWidget(category_label)

            # Progress bar with a styled appearance
            progress_bar = QProgressBar()
            progress_bar.setMaximum(self.budget_data[category]['budget'])
            progress_bar.setValue(self.budget_data[category]['spent'])
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: 1px solid #aaa;
                    border-radius: 5px;
                    background-color: #eee;
                }
                QProgressBar::chunk {
                    background-color: #76c7c0;
                    width: 20px;
                }
            """)
            category_layout.addWidget(progress_bar)

            # Label to show remaining budget with better styling
            remaining_label = QLabel(f"Remaining: {self.budget_data[category]['budget']} - Spent: 0")
            remaining_label.setStyleSheet("font-size: 14px; color: #555;")
            category_layout.addWidget(remaining_label)

            # Input box for expense amount
            expense_input = QLineEdit()
            expense_input.setPlaceholderText(f"Add expense to {category}")
            expense_input.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 5px; border: 1px solid #aaa;")
            category_layout.addWidget(expense_input)

            # Input box for description (optional)
            description_input = QLineEdit()
            description_input.setPlaceholderText(f"Description for {category} (optional)")
            description_input.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 5px; border: 1px solid #aaa;")
            category_layout.addWidget(description_input)

            # Date picker for the expense (defaults to today)
            date_input = QDateEdit()
            date_input.setDate(QDate.currentDate())
            date_input.setCalendarPopup(True)  # Popup calendar for better UX
            date_input.setStyleSheet("padding: 8px; font-size: 14px; border-radius: 5px; border: 1px solid #aaa;")
            category_layout.addWidget(date_input)

            # Button to add expense with improved styling
            add_expense_button = QPushButton(f"Add to {category}")
            add_expense_button.setStyleSheet("""
                QPushButton {
                    background-color: #009688;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #00796b;
                }
            """)
            add_expense_button.clicked.connect(lambda checked, cat=category: self.add_expense(cat))
            category_layout.addWidget(add_expense_button)

            scroll_layout.addLayout(category_layout)

            # Store widgets for updating later
            self.budget_widgets[category] = {
                'progress_bar': progress_bar,
                'remaining_label': remaining_label,
                'expense_input': expense_input,
                'description_input': description_input,
                'date_input': date_input
            }

        # Add export button with improved styling
        export_button = QPushButton("Export Budget Data")
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 12px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        export_button.clicked.connect(self.export_budget_data)  # Connect to the export function
        scroll_layout.addWidget(export_button)

        # Set scroll area content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def add_expense(self, category):
        """Add an expense to the selected category."""
        expense_input = self.budget_widgets[category]['expense_input']
        description_input = self.budget_widgets[category]['description_input']
        date_input = self.budget_widgets[category]['date_input']

        expense = expense_input.text()
        description = description_input.text() if description_input.text() else category
        date = date_input.date().toString("yyyy-MM-dd")

        if expense.isdigit():
            expense = int(expense)
            self.budget_data[category]['spent'] += expense

            # Emit the signal to notify that the budget has been updated
            self.budget_updated.emit(self.budget_data)

            # Clear the input fields
            expense_input.clear()
            description_input.clear()
            date_input.setDate(QDate.currentDate())  # Reset to today's date

            # Update the UI to reflect the changes
            self.update_budget_ui(category)

    def update_budget_ui(self, category):
        """Update the progress bar and remaining label for the category."""
        budget = self.budget_data[category]['budget']
        spent = self.budget_data[category]['spent']

        # Update progress bar
        progress_bar = self.budget_widgets[category]['progress_bar']
        progress_bar.setValue(spent)

        # Update remaining budget label
        remaining_label = self.budget_widgets[category]['remaining_label']
        remaining = budget - spent
        remaining_label.setText(f"Remaining: {remaining} - Spent: {spent}")

        # Optionally, handle cases where budget is exceeded
        if spent > budget:
            remaining_label.setStyleSheet("color: red;")
        else:
            remaining_label.setStyleSheet("color: black;")

    def export_budget_data(self):
        """Export the budget data to CSV or Excel with the specified structure."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Budget Data", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if file_path:
            try:
                # Convert the budget data to a DataFrame matching the requested structure
                data = {
                    'Date': [],
                    'Category': [],
                    'Amount': [],
                    'Currency': [],
                    'Description': []
                }
                for category, values in self.budget_data.items():
                    date_input = self.budget_widgets[category]['date_input']
                    description_input = self.budget_widgets[category]['description_input']

                    date = date_input.date().toString("yyyy-MM-dd")
                    description = description_input.text() if description_input.text() else category

                    data['Date'].append(date)  # User-specified date
                    data['Category'].append(category)
                    data['Amount'].append(values['spent'])  # Total spent amount
                    data['Currency'].append('USD')  # Default currency
                    data['Description'].append(description)  # User-specified or default description

                df = pd.DataFrame(data)

                # Save as CSV or Excel depending on file extension
                if file_path.endswith('.csv'):
                    df.to_csv(file_path, index=False)
                else:
                    df.to_excel(file_path, index=False)

                print(f"Budget data exported successfully to {file_path}")
            except Exception as e:
                print(f"Error exporting data: {e}")
