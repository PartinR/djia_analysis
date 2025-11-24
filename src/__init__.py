# djia_analysis/src/__init__.py

# Expose data handling functions
from .data import fetch_data, clean_data

# Expose analysis functions
from .analysis import (
    calculate_return, 
    calculate_std, 
    calculate_sharpe_ratio, 
    test_hypothesis, 
    plot_results
)

# Define what gets imported if someone uses "from src import *"
__all__ = [
    'fetch_data',
    'clean_data',
    'calculate_return',
    'calculate_std',
    'calculate_sharpe_ratio',
    'test_hypothesis',
    'plot_results',
]