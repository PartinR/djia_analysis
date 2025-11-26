# djia_analysis/src/analysis.py
'''Performs financial analysis on DJIA stock data.

Calculates returns, risk (standard deviation), and sharpe ratios, and
performs hypothesis testing on the risk-return relationship.
'''

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def calculate_return(df):
    '''Calculates the annualized return for each stock.

    Args:
        df: A DataFrame containing 'stock', 'date', and 'close' columns

    Returns:
        A DataFrame with columns ['stock', 'annualized_return'].
        Returns an empty DataFrame if input is empty. 
    '''
    if df.empty:
        return df

    df = df.sort_values(by=['stock', 'date'])
    df['weekly_return'] = df.groupby('stock')['close'].pct_change()

    df_return = df.groupby('stock')['weekly_return'].mean().reset_index(name='avg_weekly_return')

    # Annualize the weekly_returns (52 weeks in a year)
    df_return['annualized_return'] = df_return['avg_weekly_return'] * 52

    return df_return[['stock','annualized_return']]

def calculate_std(df):
    """Calculates the annualized standard deviation (risk) for each stock.

    Args:
        df: A DataFrame containing 'stock', 'date', and 'close' columns.

    Returns:
        A DataFrame with columns ['stock', 'annualized_std'].
        Returns an empty DataFrame if input is empty.
    """
    if df.empty:
        return df

    df = df.sort_values(by=['stock', 'date'])
    df['weekly_return'] = df.groupby('stock')['close'].pct_change()

    # Calculate the standard deviation
    df_std = df.groupby('stock')['weekly_return'].std().reset_index(name='avg_weekly_std')

    # Annualize the volatility: multiply by sqrt(52) because variance scales with time
    df_std['annualized_std'] = df_std['avg_weekly_std'] * np.sqrt(52)

    return df_std[['stock','annualized_std']]

def calculate_sharpe_ratio(df_return, df_std, risk_free_rate=0.02):
    """Calculates the sharpe ratio for each stock.

    Formula: (Annualized Return - Risk Free Rate) / Annualized Risk

    Args:
        df_return: DataFrame with 'stock' and 'annualized_return'.
        df_std: DataFrame with 'stock' and 'annualized_std'.
        risk_free_rate: The theoretical return of an investment with zero risk.

    Returns:
        A merged DataFrame including the calculated 'sharpe_ratio'.
    """
    df_merge = pd.merge(df_return, df_std, on='stock', how='inner')
    df_merge['sharpe_ratio'] = (
        (df_merge['annualized_return'] - risk_free_rate) / df_merge['annualized_std']
    )

    return df_merge[['stock', 'annualized_return', 'annualized_std', 'sharpe_ratio']]

def test_hypothesis(df_sharpe_ratio, alpha=0.05):
    """Tests the null hypothesis that there is no linear relationship between risk and return.
    
    Performs a linear regression. The Alternative Hypothesis (Ha) is that
    slope > 0 (higher risk leads to higher return).

    Args:
        df_sharpe_ratio: DataFrame containing 'annualized_std' and 'annualized_return'.
        alpha: The significance level for the test. Defaults to 0.05.

    Returns:
        The slope and intercept of the linear regression line.
    """
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        df_sharpe_ratio['annualized_std'],
        df_sharpe_ratio['annualized_return']
    )

    # Scipy returns a two-sided p-value. For Ha: slope > 0, we halve it.
    # If slope is negative, p-value for Ha > 0 is 1.0 (no evidence).
    if slope > 0:
        p_value_one_sided = p_value / 2
    else:
        p_value_one_sided = 1.0

    print("\n--- Hypothesis Test Results ---")
    print(f"Regression Slope: {slope:.2f}")
    print(f"R-Squared Value: {r_value**2:.2f}")
    print(f"One-Sided P-Value: {p_value_one_sided:.2f}")

    if p_value_one_sided < alpha and slope > 0:
        print(f"Conclusion: Reject Null Hypothesis at {alpha:.0%} level.")
        print("Evidence supports that higher risk leads to higher returns.")
    else:
        print(f"Conclusion: Fail to reject Null Hypothesis at {alpha:.0%} level.")
        print("Insufficient evidence that higher risk leads to higher returns.")

    return slope, intercept

def plot_results(df, slope, intercept):
    '''Plots the risk vs. return scatter plot with the regression line.
    
    Args:
        df: DataFrame containing 'annualized_std', 'annualized_return',
            and 'sharpe_ratio'
        slope: The slope of the regression line (from hypothesis_test).
        interept: The y-intercpet of the regression line.
    '''
    plt.figure(figsize=(10,8))

    scatter = plt.scatter(
        x=df['annualized_std'],
        y=df['annualized_return'],
        s=100,
        c='steelblue'
    )

    x_line = np.array([df['annualized_std'].min(), df['annualized_std'].max()])
    y_line = slope * x_line + intercept

    plt.plot(
        x_line,
        y_line,
        color='firebrick',
        label=f'Regression Line (Slope: {slope:.2f})'
    )
    
    plt.grid(axis='both', linestyle='--', linewidth=0.5)
    plt.title('DJIA: Annualized Risk vs. Return', fontsize=14)
    plt.xlabel('Annualized Risk (Standard Deviation)', fontsize=12)
    plt.ylabel('Annualized Return', fontsize=12)
    plt.title('Scatter Plot with Regression Line')

    plt.show()

def plot_bubble(df):
    '''Plots the relationship: Risk (X), Return (Y), Sharpe Ratio (Color and Size).

    Args:
        df: DataFrame containing 'annualized_std', 'annualized_return',
            and 'sharpe_ratio'.
    '''
    plt.figure(figsize=(10,8))

    # Increase the size of the bubbles so they are more visible
    bubble_size = df['sharpe_ratio'].abs() * 1000

    scatter = plt.scatter(
        x=df['annualized_std'],
        y=df['annualized_return'],
        s=bubble_size,
        c=df['sharpe_ratio'],
        alpha=0.6
    )

    cbar = plt.colorbar(scatter)
    cbar.set_label('Sharpe Ratio')

    plt.grid(axis='both', linestyle='--', linewidth=0.5)
    plt.title('DJIA: Annualized Risk vs. Return', fontsize=14)
    plt.xlabel('Annualized Risk (Standard Deviation)', fontsize=12)
    plt.ylabel('Annualized Return', fontsize=12)
    plt.title('Bubble Chart')

    plt.show()

def plot_bar(df):
    '''Plots a two axis chart listing stocks in order of sharpe ratio
    and showing annualized standard deviation for context.

    Args:
        df: DataFrame containing 'annualized_std', 'annualized_return',
            and 'sharpe_ratio'.
    '''
    df_sort = df.sort_values(by='sharpe_ratio', ascending=False)
    fig, ax1 = plt.subplots(figsize=(14,6))

    ax1.set_xlabel('Stocks')
    ax1.set_ylabel('Sharpe Ratio')

    bar_color = np.where(df_sort['sharpe_ratio'] > 0, 'steelblue', 'firebrick')
    ax1.bar(
        df_sort['stock'], 
        df_sort['sharpe_ratio'], 
        color=bar_color 
    )

    # Line at sharpe ratio = 0
    ax1.axhline(0, color='gray', linewidth=0.8) 
    plt.xticks(rotation=45, ha='right')
    plt.title('Dual-Axis Bar Chart')

    # Add line to represent standard deviation
    ax2 = ax1.twinx()
    ax2.set_ylabel('Annualized Standard Deviation (Risk)')
    ax2.plot(
        df_sort['stock'],
        df_sort['annualized_std'],
        color='black',
        linestyle='--'
    )

    fig.tight_layout()
    plt.show()