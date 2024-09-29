import pandas as pd

def import_excel(file_path):
    """Function to import and read Excel or CSV data."""
    try:
        if file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
        else:
            # Specify 'openpyxl' as the engine for reading .xlsx files
            data = pd.read_excel(file_path, engine='openpyxl')
        return data
    except Exception as e:
        print(f"Error importing file: {e}")
        return None
