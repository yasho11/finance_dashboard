# Interactive Finance Dashboard

The **Interactive Finance Dashboard** is a comprehensive tool for managing and visualizing your personal or business finances. It allows users to upload transaction data, visualize it through a variety of charts, predict future expenses using machine learning models, track budgets with real-time updates, and export data in different formats. The application includes comparison across different time periods (months, years), export functionality (PDF/Excel), and integrates with currency conversion APIs.

---

## Table of Contents

- [Features](#features)
- [Objectives](#objectives)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
    - [Clone the Repository](#clone-the-repository)
    - [Set Up the Environment](#set-up-the-environment)
    - [Install Dependencies](#install-dependencies)
    - [Configure API Keys and Environment Variables](#configure-api-keys-and-environment-variables)
    - [Set Up Google Calendar Credentials](#set-up-google-calendar-credentials)
- [Running the Dashboard](#running-the-dashboard)
- [Using the Dashboard](#using-the-dashboard)
    - [Uploading a File](#uploading-a-file)
    - [Viewing Charts and KPIs](#viewing-charts-and-kpis)
    - [Budget Tracking](#budget-tracking)
    - [Expense Prediction Using Machine Learning](#expense-prediction-using-machine-learning)
    - [Comparison Across Time Periods](#comparison-across-time-periods)
    - [Export Functionality](#export-functionality)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)
- [Code](#code)

---

## Overview

The **Interactive Finance Dashboard** allows users to manage their financial data easily and effectively. It includes a range of features, from basic expense tracking to advanced financial forecasting with machine learning. The dashboard is designed for both individuals and businesses, providing insights into past spending habits and predictions for future expenses.

This tool offers a holistic approach to financial management by combining data visualization, machine learning, budget tracking, and export functionality.

---

## Features

- **Data Upload**: Users can upload CSV or Excel files containing financial transaction data.
- **KPI Tracking**: Displays total expenses, total categories, and the top spending category.
- **Charts**: Provides bar charts, line charts, and donut charts for data visualization.
- **Budget Tracker**: Allows users to set budgets for different categories and tracks real-time spending using signals/slots.
- **Comparison by Time Periods**: Enables comparison of expenses across different time frames like months and years.
- **Machine Learning**: Implements machine learning models to predict future expenses based on historical data.
- **Export Functionality**: Export data in PDF or Excel format and includes currency conversion via API.
- **Real-time Updates**: Provides real-time updates to the UI with budget and prediction results.

---

## Objectives

- **Data Visualization**: Allow users to visualize their past and present spending with ease.
- **Budget Tracking**: Help users manage their budgets by tracking category-wise expenses.
- **Expense Forecasting**: Use machine learning to predict future expenses and alert users to potential overspending.
- **Comparison Across Time**: Provide the ability to analyze and compare spending across different time periods.
- **Export and Currency Conversion**: Allow users to export data and convert currencies for international transactions.
- **User-friendly Interface**: Provide an intuitive and simple interface for non-technical users.

---

## Prerequisites

Before running the project, make sure you have the following:

- **Python 3.7+**
- **Pip** (Python package manager)
- **Git** (to clone the repository)
- **Excel or CSV files** with financial data containing at least the following columns:
    - `Date`: The date of the transaction
    - `Category`: The category of the expense
    - `Amount`: The amount spent in the transaction

---

## Installation and Setup

Follow these steps to install and set up the project on your local machine.

### Clone the Repository

1. Open your terminal and run the following command to clone the repository:

    ```bash
    git clone https://github.com/yourusername/finance-dashboard.git
    ```

2. Navigate to the project directory:

    ```bash
    cd finance-dashboard
    ```

### Set Up the Environment

It’s recommended to create a virtual environment for the project.

1. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

### Install Dependencies

1. Install the required dependencies listed in the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

### Configure API Keys and Environment Variables

For currency conversion and any other external services, add your API keys in a `.env` file:

- Example:

    ```plaintext
    API_KEY=your_api_key
    ```

---

## Running the Dashboard

Once the setup is complete, run the following command to start the dashboard:

```bash
python app.py

```
---
