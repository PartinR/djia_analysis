#djia_analysis/src/main.py

# Import statements
from .data import fetch_data, clean_data
from .analysis import calculate_return, calculate_std, calculate_sharpe_ratio, test_hypothesis, plot_results

def main():
    # Data handling
    df_raw = fetch_data()
    df_clean = clean_data(df_raw)

    # Calculate returns
    df_return = calculate_return(df_clean)

    # Calculate standard deviation
    df_std = calculate_std(df_clean)

    print(df_return)
    print()
    print(df_std)

    # Calculate sharpe ratio
    df_sharpe = calculate_sharpe_ratio(df_return, df_std)
    print(df_sharpe)

    slope, intercept = test_hypothesis(df_sharpe)

    plot_results(df_sharpe, slope, intercept)

if __name__ == "__main__":
    main()