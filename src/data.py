# djia_analysis/src/data.py
'''Data loading and cleaning module for DJIA analysis.'''

import pandas as pd

# Constants
FILE_PATH = '/Users/racepartin/repos/djia_analysis/data/dow_jones_index.data'

def fetch_data():
    """Loads the DJIA dataset from the local CSV file.

    Reads the file specified in the global FILE_PATH constant. Handles
    errors if the file is missing.

    Returns:
        pd.DataFrame: A DataFrame containing the raw stock data. 
        Returns an empty DataFrame if the file is not found.
    """
    try:
        df = pd.read_csv(FILE_PATH)
        print("Data successfully loaded.")
        return df
    except FileNotFoundError:
        print(f"ERROR: File cannot be located at {FILE_PATH}. Check file path.")
        return pd.DataFrame()

def clean_data(df):
    """Prepares the raw DataFrame for analysis.

    Performs the following cleaning operations:
    1. Converts the 'date' column to datetime objects.
    2. Removes '$' symbols from price columns (e.g., 'close', 'open').
    3. Converts those price columns to numeric data types.

    Args:
        df: The raw DataFrame loaded via fetch_data().

    Returns:
        pd.DataFrame: The cleaned DataFrame with correct data types.
        Returns an empty DataFrame if input is empty.
    """
    if df.empty:
        return df

    # Convert 'date' to datetime object for analysis
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    clean_price_columns = [
        'open', 'high', 'low', 'close', 
        'next_weeks_open', 'next_weeks_close'
    ]

    # Clean relevant columns by removing '$'
    for col in clean_price_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace('$', '', regex=False)
                df[col] = pd.to_numeric(df[col])

    return df