# DJIA Analysis

### Overview
This project involves analyzing the individual stocks inside the **Dow Jones Industrial Average (DJIA)** to determine whether **higher risk leads to higher returns** inside of this specific world of blue-chip stocks. The pipeline will ingest historical price data, calculate metrics for risk (e.g., standard deviation/volatility) and return (e.g., average return), and use statistical modeling to test the relationship.

### Project Goal
To design and implement:
- A **data ingestion and cleaning module** that reliably fetches and processes historical stock data for all 30 DJIA components.
- A **financial metrics module** to calculate annualized **risk (volatility)** and **return** for each stock.
- A **statistical model** to quantify the relationship between calculated risk and return.
- A **single-point runner script** to execute the entire analysis and generate a final conclusion report.

### Technologies
- Language: Python
- Libraries: Pandas, NumPy, Matplotlib, SciPy

## File Structure
```text
djia_analysis/
├── data/
│   └── dow_jones_index.data    # Raw dataset from UCI Machine Learning Repository
├── src/
│   ├── __init__.py             # Exposes functions for package import
│   ├── analysis.py             # Contains math (Sharpe ratio, Std Dev) and plotting functions
│   ├── data.py                 # Handles data loading and cleaning (removes '$', fixes dates)
│   └── main.py                 # Entry point: orchestrates the analysis pipeline
├── Partin_CMPS240_Report.pdf   # Final project report
└── README.md                   # Project documentation