from data_handler.stock_data import StockDataHandler
from metrics_calculator.calculator import StockMetricsCalculator
from visualizer.plots import StockVisualizer
import streamlit as st
import plotly.graph_objs as go

from streamlit_autorefresh import st_autorefresh

class StockDashboardApp:
    def __init__(self):
        self.api_key = st.secrets["api"]["iex_key"]
        self.api_base_url = "https://cloud.iexapis.com/stable/"
        self.data_handler = StockDataHandler(self.api_key, self.api_base_url)
        self.calculator = StockMetricsCalculator()
        self.visualizer = StockVisualizer()

    def run(self):
        st.set_page_config(page_title="Stock Dashboard", layout="wide", page_icon="📈")
        # auto refresh after a certain interval. turn off because of API limit. 
        # interval = 60000  # in milliseconds
        # st_autorefresh(interval=interval, key='data_refresh')

        st.markdown("<style>.stRadio > div {display: flex; flex-direction: column; gap: 10px; margin-bottom: 10px;}</style>", unsafe_allow_html=True)
        st.sidebar.markdown("# Stock Dashboard")
        st.sidebar.markdown("Please select a stock symbol and duration from the options below to view detailed stock data and charts.")

        popular_symbols = ["AAPL", "GOOGL", "MSFT", "META", "NVDA"]
        new_symbol = st.sidebar.text_input("Input a new ticker:")
        if new_symbol:
            popular_symbols.append(new_symbol.upper())
            st.sidebar.success(f"Added {new_symbol.upper()} to the list")
        symbol = st.sidebar.selectbox("Select a ticker:", popular_symbols, index=2)
        st.title(f"{symbol}")
        time_range_options = ["5d","1m", "3m", "6m", "1y", "2y", "5y", "YTD", "max"]
        selected_time_range = st.sidebar.selectbox("Select period:", time_range_options, index=2)

        show_candlestick = st.sidebar.checkbox("Candlestick Chart", value=True)
        show_summary = st.sidebar.checkbox("Summary", value=True)
        show_moving_averages = st.sidebar.checkbox("Moving Averages", value=False)
        show_bollinger_bands = st.sidebar.checkbox("Bollinger Bands", value=False)
        show_obv = st.sidebar.checkbox("On-Balance Volume", value=False)
        show_rsi = st.sidebar.checkbox("Relative Strength Index (RSI)", value=False)
        show_macd = st.sidebar.checkbox("Moving Average Convergence Divergence (MACD)", value=False)
        show_atr = st.sidebar.checkbox("Average True Range (ATR)", value=False)
        show_vwap = st.sidebar.checkbox("Volume Weighted Average Price (VWAP)", value=False)
        show_volatility = st.sidebar.checkbox("Historical Volatility", value=False)

        if symbol:
            stock_data, time_range = self.data_handler.get_stock_data(symbol, selected_time_range)
            if stock_data is not None:
                price_difference, percentage_difference = self.calculator.calculate_price_difference(stock_data)
                latest_close_price = stock_data.iloc[-1]["Close"]
                max_52_week_high = stock_data["High"].max()
                min_52_week_low = stock_data["Low"].min()

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Close Price", f"${latest_close_price:.2f}")
                with col2:
                    st.metric("Price Difference", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
                with col3:
                    st.metric("52-Week High", f"${max_52_week_high:.2f}")
                with col4:
                    st.metric("52-Week Low", f"${min_52_week_low:.2f}")

                if show_candlestick:
                    candlestick_chart = self.visualizer.plot_candlestick(stock_data, symbol, time_range)
                    st.subheader("Candlestick Chart")
                    st.plotly_chart(candlestick_chart, use_container_width=True)

                if show_moving_averages:
                    stock_data = self.calculator.calculate_moving_averages(stock_data)
                    ma_fig = self.visualizer.plot_moving_averages(stock_data)
                    st.plotly_chart(ma_fig, use_container_width=True)
                if show_bollinger_bands:
                    stock_data = self.calculator.calculate_bollinger_bands(stock_data)
                    bb_fig = self.visualizer.plot_bollinger_bands(stock_data)
                    st.plotly_chart(bb_fig, use_container_width=True)

                if show_obv:
                    stock_data = self.calculator.calculate_on_balance_volume(stock_data)
                    obv_fig = self.visualizer.plot_obv(stock_data)
                    st.plotly_chart(obv_fig, use_container_width=True)

                if show_rsi:
                    stock_data = self.calculator.calculate_rsi(stock_data)
                    rsi_fig = self.visualizer.plot_rsi(stock_data)
                    st.plotly_chart(rsi_fig, use_container_width=True)

                if show_macd:
                    stock_data = self.calculator.calculate_macd(stock_data)
                    macd_fig = self.visualizer.plot_macd(stock_data)
                    st.plotly_chart(macd_fig, use_container_width=True)

                if show_atr:
                    stock_data = self.calculator.calculate_atr(stock_data)
                    atr_fig = self.visualizer.plot_atr(stock_data)
                    st.plotly_chart(atr_fig, use_container_width=True)

                if show_vwap:
                    stock_data = self.calculator.calculate_vwap(stock_data)
                    vwap_fig = self.visualizer.plot_vwap(stock_data)
                    st.plotly_chart(vwap_fig, use_container_width=True)

                if show_volatility:
                    stock_data = self.calculator.calculate_historical_volatility(stock_data)
                    vol_fig = self.visualizer.plot_volatility(stock_data)
                    st.plotly_chart(vol_fig, use_container_width=True)

                if show_summary:
                    st.subheader("Summary")
                    st.dataframe(stock_data.tail())

                st.download_button("Download Stock Data Overview", stock_data.to_csv(index=True), file_name=f"{symbol}_stock_data.csv", mime="text/csv")

if __name__ == "__main__":
    app = StockDashboardApp()
    app.run()
