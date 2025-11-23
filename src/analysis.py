# djia_analysis/src/analysis.py

# Import statements
import pandas as pd
import numpy as np

def calculate_return(df):
    '''
    Calculates the annualized return for each stock.
    '''

    if df.empty:
        return df

    # Sort and create weekly_return column using date and pct_change
    df = df.sort_values(by=['stock', 'date'])
    df['weekly_return'] = df.groupby('stock')['close'].pct_change()

    # Calculate the mean of the weekly_return's
    df_return = df.groupby('stock')['weekly_return'].mean().reset_index(name='avg_weekly_return')

    # Annualize the weekly_return's
    df_return['annualized_return'] = df_return['avg_weekly_return'] * 52

    return df_return[['stock','annualized_return']]

def calculate_std(df):
    '''
    Calculate the annualized standard deviation for each stock.
    '''

    if df.empty:
        return df

     # Sort and create weekly_return column using date and pct_change
    df = df.sort_values(by=['stock', 'date'])
    df['weekly_return'] = df.groupby('stock')['close'].pct_change()

    # Calculate the standard deviation of the weekly_return's
    df_std = df.groupby('stock')['weekly_return'].std().reset_index(name='avg_weekly_std')

    # Annualize the standard deviation
    df_std['annualized_std'] = df_std['avg_weekly_std'] * np.sqrt(52)

    return df_std[['stock','annualized_std']]

def calculate_sharpe_ratio(df_return, df_std, risk_free_rate=0.02):
    '''
    Calculates the sharpe ratio for each stock.
    Sharpe ratio = (annualized_return - risk_free_rate) / annualized_std
    '''

    # Merge df_returns and df_std
    df_merge = pd.merge(df_return, df_std, on='stock', how='inner')

    # Calculate the sharpe_ratio
    df_merge['sharpe_ratio'] = (df_merge['annualized_return'] - risk_free_rate) / df_merge['annualized_std']

    return df_merge[['stock', 'annualized_return', 'annualized_std', 'sharpe_ratio']]