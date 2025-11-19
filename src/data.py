# djia_analysis/src/data.py

# Import statements
import pandas as pd

# File path to be read
path = '/Users/racepartin/repos/djia_analysis/data/dow_jones_index.data'

def fetch_data():
    '''
    Reads locally stored data using hardcoded path.
    '''

    try:
        df = pd.read_csv(path)
        print('Data successfully loaded.')
        return df
    except FileNotFoundError:
        print('ERROR: File cannot be located. Check file path.')
        return pd.DataFrame()

def clean_data(df):
    '''
    Extract useful information from the data.
    '''

    if df.empty:
        return df
    
    # Convert 'date' to datetime object for analysis
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    clean_price_columns = ['open', 'high', 'low', 'close', 'next_weeks_open', 'next_weeks_close']

    # Clean relevant columns by removing '$'
    for col in clean_price_columns:
        if col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.replace('$', '', regex=False)
                df[col] = pd.to_numeric(df[col])

    return df