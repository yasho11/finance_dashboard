from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QProgressBar, QWidget
from PySide6.QtCore import Qt, Signal

class BudgetTrackerView(QWidget):
    # Signal emitted when an expense is added or updated
    budget_updated = Signal(dict)

    def __init__(self):
        super().__init__()

        # Sample budget categories and initial amounts
        self.budget_data = {
            'Groceries': {'budget': 500, 'spent': 0},
            'Rent': {'budget': 1000, 'spent': 0},
            'Utilities': {'budget': 200, 'spent': 0}
        }

        # Main layout
        layout = QVBoxLayout()

        # Budget tracking widgets (labels, input fields, progress bars)
        self.budget_widgets = {}
        for category in self.budget_data:
            category_layout = QVBoxLayout()

            # Label for the category
            category_label = QLabel(f"{category} Budget")
            category_label.setStyleSheet("font-size: 16px;")
            category_layout.addWidget(category_label)

            # Progress bar to show how much of the budget is spent
            progress_bar = QProgressBar()
            progress_bar.setMaximum(self.budget_data[category]['budget'])
            progress_bar.setValue(self.budget_data[category]['spent'])
            category_layout.addWidget(progress_bar)

            # Label to show remaining budget
            remaining_label = QLabel(f"Remaining: {self.budget_data[category]['budget']} - Spent: 0")
            category_layout.addWidget(remaining_label)

            # Line edit to input new expenses
            expense_input = QLineEdit()
            expense_input.setPlaceholderText(f"Add expense to {category}")
            category_layout.addWidget(expense_input)

            # Button to add expense
            add_expense_button = QPushButton(f"Add to {category}")
            add_expense_button.clicked.connect(lambda checked, cat=category: self.add_expense(cat))
            category_layout.addWidget(add_expense_button)

            layout.addLayout(category_layout)

            # Store widgets for updating later
            self.budget_widgets[category] = {
                'progress_bar': progress_bar,
                'remaining_label': remaining_label,
                'expense_input': expense_input
            }

        self.setLayout(layout)

    def add_expense(self, category):
        """Add an expense to the selected category."""
        expense_input = self.budget_widgets[category]['expense_input']
        expense = expense_input.text()

        if expense.isdigit():
            expense = int(expense)
            self.budget_data[category]['spent'] += expense

            # Emit the signal to notify that the budget has been updated
            self.budget_updated.emit(self.budget_data)

            # Clear the input field
            expense_input.clear()

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
