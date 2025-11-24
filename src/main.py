#djia_analysis/src/main.py
'''Main execution program for DJIA Risk/Return Analysis'''

from .data import fetch_data, clean_data
from .analysis import (
    calculate_return, 
    calculate_std, 
    calculate_sharpe_ratio, 
    test_hypothesis, 
    plot_results,
    plot_bubble,
    plot_bar
)

# Constants
RISK_FREE_RATE = 0.00
ALPHA = 0.05

def main():
    '''Executes the financial analysis pipeline.'''
    print("--- Starting DJIA Analysis ---")

    # 1. Data Pipleine
    print("Fetching and cleaning data...")
    df_raw = fetch_data()
    df_clean = clean_data(df_raw)

    # 2. Calculate Pipeline
    print("Calculating metrics...")
    df_return = calculate_return(df_clean)
    df_std = calculate_std(df_clean)

    df_sharpe = calculate_sharpe_ratio(
        df_return, 
        df_std,
        risk_free_rate = RISK_FREE_RATE
    )

    # 3. Hypothesis testing
    slope, intercept = test_hypothesis(df_sharpe, alpha=ALPHA)

    # 4. Visualization
    print("Generating Plots...")
    plot_results(df_sharpe, slope, intercept)
    plot_bubble(df_sharpe)
    plot_bar(df_sharpe)

if __name__ == "__main__":
    main()