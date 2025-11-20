#djia_analysis/src/main.py

# Import statements
from .data import fetch_data, clean_data
from .analysis import calculate_returns

def main():
    df_raw = fetch_data()  
    df_clean = clean_data(df_raw)
    df_return = calculate_returns(df_clean)
    print(df_return)

if __name__ == "__main__":
    main()