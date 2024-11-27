from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
import streamlit as st

@st.cache_data
def forecast_stock_data(df_train, period):
    # Prepare the DataFrame for Prophet
    df_train['ds'] = pd.to_datetime(df_train['ds']).dt.tz_localize(None)

    # Initialize and fit the Prophet model
    m = Prophet()
    m.fit(df_train)

    # Create a future DataFrame
    future = m.make_future_dataframe(periods=period)

    # Predict the future
    forecast = m.predict(future)

    # Ensure yhat and bounds are numeric
    for col in ['yhat', 'yhat_lower', 'yhat_upper']:
        forecast[col] = pd.to_numeric(forecast[col], errors='coerce')

    # Drop rows with NaN values
    forecast.dropna(subset=['yhat', 'yhat_lower', 'yhat_upper'], inplace=True)

    return m, forecast


