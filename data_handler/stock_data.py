import requests
import pandas as pd
import streamlit as st 

API_KEY = st.secrets["api"]["iex_key"]
API_BASE_URL = "https://cloud.iexapis.com/stable/"

class StockDataHandler:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get_stock_data(self, symbol, selected_time_range="1y"):
        params = {"token": self.api_key}
        response = requests.get(f"{self.base_url}stock/{symbol}/chart/{selected_time_range}", params=params)
        data = response.json()

        if "error" not in data:
            stock_data = pd.DataFrame(data)
            if not stock_data.empty:
                stock_data["date"] = pd.to_datetime(stock_data["date"])
                stock_data.set_index("date", inplace=True)
                stock_data = stock_data[["open", "high", "low", "close", "volume"]]
                stock_data.columns = ["Open", "High", "Low", "Close", "Volume"]
                return stock_data, selected_time_range
        else:
            st.error(f"No available data for symbol: {symbol} for {selected_time_range} time range")
            return None, None
