import streamlit as st
from datetime import date
import time
from streamlit_free_text_select import st_free_text_select # type: ignore
from prophet.plot import plot_plotly, plot_components_plotly
from data_processing import preprocess_data
from forecasting import forecast_stock_data
from visualization import plot_stock_data
import yfinance as yf


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

def main():
    st.title("📈 Stockast")
    st.markdown(
        """ 
        *Analyze historical data and forecast future trends with ease.*
        """
    )

    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'TSLA', 'NVDA']

    try:
        selected_stock = st_free_text_select(
            label='Select or type dataset for prediction:',
            options=stocks[::-1],
            index=None,
            format_func=lambda x: x.upper(),
            placeholder=stocks[-1],
            disabled=False,
            delay=300,
            label_visibility="visible",
        ).upper()
    except:
        selected_stock = stocks[-1]

    # Period duration slider
    n_years = st.slider(f'Years for prediction:', 1, 10)
    period = n_years * 365

    

    if st.button('Generate Forecast'):
        # Fetch and preprocess data
        data = fetch_stock_data(selected_stock)
        df_train = preprocess_data(data)

        if data.empty:
            st.error(f'Unable to retrieve data for {selected_stock}. Please check that you have selected or entered the correct value.')
        else:
            st.subheader('Raw data')
            st.write(data.tail())
            plot_stock_data(data)

            # Perform forecasting
            model, forecast = forecast_stock_data(df_train, period)

            # Display forecast data
            st.subheader('Forecast data')
            st.write(forecast.tail())

            # Plot forecast and components
            st.write(f'Forecast plot for {n_years} years')
            fig1 = plot_plotly(model, forecast)
            st.plotly_chart(fig1)

            st.write("Forecast components")
            fig2 = plot_components_plotly(model, forecast)
            st.write(fig2)


@st.cache_data(ttl=86400)
def fetch_stock_data(ticker):
    start_time = time.time()
    data = yf.download(ticker, START, TODAY)
    print(f"Data fetching took {time.time() - start_time:.2f} seconds")
    data.reset_index(inplace=True)

    # Flatten the MultiIndex columns
    data.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in data.columns]

    # Rename columns to remove the ticker
    data.columns = [col.replace(f' {ticker}', '') for col in data.columns]

    return data

if __name__ == '__main__':
    main()
