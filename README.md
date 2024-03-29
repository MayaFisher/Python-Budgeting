# Personal Finance Dashboard

## Description

The Personal Finance Dashboard is an intuitive Python tool designed to help users visualize and manage their finances. Leveraging powerful libraries like pandas, numpy, tkinter, and panel, it provides an insightful overview of your financial activities including expenses, income, and savings.

## Features

- **File Browsing**: Easily select and import financial data (.csv format).
- **Data Cleaning and Processing**: Ensures your financial data is accurate and reliable.
- **Dynamic Categorization**: Transactions are automatically sorted into categories like Groceries, Rent, and Eating Out.
- **Monthly Summary**: Get a snapshot of your monthly financial activities, highlighting income, expenses (recurring and non-recurring), and savings.
- **Interactive Dashboard**: Explore your financial data through engaging charts and tables.

## Installation

Ensure you have Python installed on your machine. Install the required libraries using:

```bash
pip install pandas numpy panel hvplot holoviews datetime
```

## Usage

- **Start the Program**: Execute the script to open a file dialog and choose your CSV file with transaction data.
- **Data Processing**: The script will process and categorize your transactions automatically.
- **View Dashboard**: Interact with your data using the generated dashboard filled with various widgets and visualizations.

## File Format

Your financial data should be in a CSV file with the following columns:

- Date
- Description
- Amount
- Transaction Type
- Account Name

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Make your changes.
3. Submit a pull request with a clear description of your improvements.
