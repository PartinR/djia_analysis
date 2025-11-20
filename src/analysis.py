# djia_analysis/src/analysis.py

# Import statements
import pandas as pd
import numpy as np

def calculate_returns(df):
    '''
    Calculates the annualized return for each stock.
    '''

    if df.empty():
        return df

    # Sort and create weekly_return column using date and pct_change
    df = df.sort_values(by=['stock', 'date'])
    df['weekly_return'] = df.groupby('stock')['close'].pct_change()

    # Calculate the mean of the weekly_return's
    df_return = df.groupby('stock')['weekly_return'].mean().reset_index(name='avg_weekly_return')

    # Annualize the weekly_return's
    df_return['annualized_return'] = df_return['avg_weekly_return'] * 52

    return df_return[['stock','annualized_return']]