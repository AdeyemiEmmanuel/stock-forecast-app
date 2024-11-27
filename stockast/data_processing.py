import pandas as pd
import streamlit as st

@st.cache_data
def preprocess_data(data):
    """
    Prepares the stock data for Prophet forecasting by renaming
    the columns and selecting relevant data.
    """
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    # Ensure 'y' is numeric
    df_train['y'] = pd.to_numeric(df_train['y'], errors='coerce')

    # Drop rows with NaN values (if any)
    df_train = df_train.dropna()

    return df_train
