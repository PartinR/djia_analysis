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
