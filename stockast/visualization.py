from plotly import graph_objs as go
import streamlit as st


@st.cache_data
def plot_stock_data(data):
    """
    Plots raw stock data (Open and Close prices) using Plotly.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)
