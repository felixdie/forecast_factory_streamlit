import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.metrics import mean_absolute_percentage_error

def rolling_cv_mape(df, actual_col, forecast_col, min_train_size, test_size, start_date=None):
    """
    Perform rolling cross-validation to compute MAPE.

    Parameters:
    - df: DataFrame with time series data.
    - actual_col: Name of the actual values column.
    - forecast_col: Name of the forecast values column.
    - start_date: Default None; Date of format YYYY-MM-DD to start the rolling cross-validation.

    Returns:
    - mean_mape: Mean MAPE across all test sets.
    """
    # Drop forecasts
    df = df.dropna(subset=[actual_col])

    # Set timeframe
    if start_date is not None:
        df = df[df["ds"] >= start_date]

    # Train-test split (in months)
    min_train_size = min_train_size
    test_size = test_size
    mape_values = []

    # Loop through data
    for start in range(len(df) - min_train_size - test_size + 1):
        
        # Define training and test set indices
        train_end = min_train_size + start
        test_start = train_end
        test_end = test_start + test_size

        # Extract training and test sets
        train = df.iloc[:train_end]
        test = df.iloc[test_start:test_end]

        # Compute MAPE
        mape = mean_absolute_percentage_error(test[actual_col], test[forecast_col])
        mape_values.append(mape)

    mean_mape = round(np.mean(mape_values)*100, 1)
    
    return mean_mape


def plot_rolling_cv(df, actual_col, min_train_size, test_size, start_date=None):
    """
    Visualizes the rolling train-test split over a dataframe.

    Parameters:
    - df: DataFrame with time series data.
    - actual_col: Name of the actual values column.
    - min_train_size: Minimum number of months in the training set.
    - test_size: Number of months in the test set.
    - start_date: Default None; date of format YYYY-MM-DD to start the rolling cross-validation.
    """
    # Drop forecasts
    df = df.dropna(subset=[actual_col])

    # Set timeframe
    if start_date is not None:
        df = df[df["ds"] >= start_date]

    # Train-test split
    num_splits = len(df) - min_train_size - test_size + 1
    split_labels = [f"Split {i+1}" for i in range(num_splits)]

    train_lengths = []
    test_lengths = []
    unused_lengths = []

    for start in range(num_splits):
        train_end = min_train_size + start
        test_start = train_end
        test_end = test_start + test_size

        train_lengths.append(train_end)  # Train data expands
        test_lengths.append(test_size)   # Test data is fixed
        unused_lengths.append(len(df) - test_end)  # Remaining unused data

    # Visualisation
    splits_df = pd.DataFrame({
        "Train": train_lengths,
        "Test": test_lengths,
        "Unused": unused_lengths
    }, index=split_labels)

    fig, ax = plt.subplots(figsize=(10, 6))
    splits_df.plot(kind="bar", stacked=True, ax=ax, color=["blue", "orange", "gray"])
    ax.set_ylabel("Data Points")
    ax.set_xlabel("Rolling CV Splits")
    ax.set_title("Rolling Cross-Validation Train-Test Splits")
    plt.xticks(rotation=45)
    plt.legend(title="Data Type")
    st.pyplot(fig)

    # Example:
    # plot_rolling_cv(df=actuals_vs_forecast, actual_col="Actuals", start_date="2025-01-01", min_train_size=12, test_size=1)



