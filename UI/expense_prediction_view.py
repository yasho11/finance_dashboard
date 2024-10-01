from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar, QScrollArea
from PySide6.QtCore import Qt
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle

class ExpensePredictionView(QWidget):
    def __init__(self):
        super().__init__()

        # Create the scrollable layout container
        main_layout = QVBoxLayout(self)

        # Add scroll area to make the page scrollable
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(20, 20, 20, 20)
        scroll_layout.setSpacing(15)

        # Instruction label with enhanced styling
        self.instructions_label = QLabel("Upload an Excel or CSV file to predict expenses.")
        self.instructions_label.setStyleSheet("font-size: 16px; color: #333; font-weight: bold;")
        scroll_layout.addWidget(self.instructions_label)

        # Upload button with styling
        self.upload_button = QPushButton("Upload File")
        self.upload_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.upload_button.clicked.connect(self.upload_file)
        scroll_layout.addWidget(self.upload_button)

        # Result label to display predictions or errors
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 14px; color: #FF0000;")  # Red color for errors
        scroll_layout.addWidget(self.result_label)

        # Add progress bar for visual feedback during processing
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        scroll_layout.addWidget(self.progress_bar)

        # Set scroll area content
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

    def upload_file(self):
        """Function to handle file upload and predict expenses."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            try:
                # Load pre-trained model
                self.result_label.setText("Loading model... Please wait.")
                with open('prediction_expense_model/best_random_forest_(tuned)_model.pkl', 'rb') as f:
                    model = pickle.load(f)

                # Load data
                self.result_label.setText("Loading data... Please wait.")
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path)
                else:
                    data = pd.read_excel(file_path)

                # Preprocessing: Convert Date to datetime, and generate features
                if 'Date' in data.columns and 'Amount' in data.columns:
                    data['Date'] = pd.to_datetime(data['Date'])
                    data['day_of_week'] = data['Date'].dt.dayofweek  # Day of the week (0=Monday, 6=Sunday)
                    data['month'] = data['Date'].dt.month  # Month

                    # Create lag features
                    data['lag_1'] = data['Amount'].shift(1)  # Previous day's amount
                    data['lag_7'] = data['Amount'].shift(7)  # Previous week's amount

                    # Drop rows with NaN values caused by lag features
                    data.dropna(inplace=True)

                    if not data.empty and len(data) > 0:
                        # Update progress bar
                        self.progress_bar.setValue(30)

                        # Feature scaling (ensure features are in a proper range)
                        scaler = StandardScaler()
                        features_to_scale = ['lag_1', 'lag_7', 'day_of_week', 'month']
                        data_scaled = scaler.fit_transform(data[features_to_scale])

                        # Update progress bar
                        self.progress_bar.setValue(60)

                        # Make predictions
                        predictions = model.predict(data_scaled)

                        # Update progress bar
                        self.progress_bar.setValue(90)

                        # Format predictions to be more readable
                        formatted_predictions = [f"${round(pred, 2):,}" for pred in predictions]

                        # Display formatted predictions
                        self.result_label.setText(f"Predicted Expenses: {', '.join(formatted_predictions)}")
                        self.progress_bar.setValue(100)
                    else:
                        self.result_label.setText("Error: Processed data is empty after preprocessing.")
                        self.progress_bar.setValue(0)
                else:
                    self.result_label.setText("Error: The file is missing required columns ('Date' and 'Amount').")
                    self.progress_bar.setValue(0)

            except Exception as e:
                self.result_label.setText(f"Error processing file: {e}")
                self.progress_bar.setValue(0)
