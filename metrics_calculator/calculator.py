import numpy as np
import pandas as pd


class StockMetricsCalculator:
    def calculate_price_difference(self, stock_data):
        latest_price = stock_data.iloc[-1]["Close"]
        previous_price = stock_data.iloc[0]["Close"]
        price_difference = latest_price - previous_price
        percentage_difference = (price_difference / previous_price) * 100
        return price_difference, percentage_difference

    def calculate_moving_averages(self, stock_data):
        for window in [20, 50, 200]:
            stock_data[f'SMA_{window}'] = stock_data['Close'].rolling(window=window).mean()
            stock_data[f'EMA_{window}'] = stock_data['Close'].ewm(span=window, adjust=False).mean()
        return stock_data

    def calculate_bollinger_bands(self, stock_data):
        window = 20
        rolling_mean = stock_data['Close'].rolling(window=window).mean()
        rolling_std = stock_data['Close'].rolling(window=window).std()
        stock_data['Bollinger High'] = rolling_mean + (rolling_std * 2)
        stock_data['Bollinger Low'] = rolling_mean - (rolling_std * 2)
        return stock_data


    def calculate_on_balance_volume(self, stock_data):
        obv = [0]
        for i in range(1, len(stock_data)):
            if stock_data['Close'].iloc[i] > stock_data['Close'].iloc[i-1]:
                obv.append(obv[-1] + stock_data['Volume'].iloc[i])
            elif stock_data['Close'].iloc[i] < stock_data['Close'].iloc[i-1]:
                obv.append(obv[-1] - stock_data['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        stock_data['OBV'] = obv
        return stock_data


    def calculate_rsi(self, stock_data, window=14):
        delta = stock_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).fillna(0)
        loss = (-delta.where(delta < 0, 0)).fillna(0)

        avg_gain = gain.rolling(window=window, min_periods=1).mean()
        avg_loss = loss.rolling(window=window, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        stock_data['RSI'] = rsi
        return stock_data

    def calculate_macd(self, stock_data, slow=26, fast=12, signal=9):
        exp1 = stock_data['Close'].ewm(span=fast, adjust=False).mean()
        exp2 = stock_data['Close'].ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()

        stock_data['MACD'] = macd
        stock_data['Signal_Line'] = signal_line
        return stock_data
    def calculate_atr(self, stock_data, window=14):
        high_low = stock_data['High'] - stock_data['Low']
        high_close = np.abs(stock_data['High'] - stock_data['Close'].shift())
        low_close = np.abs(stock_data['Low'] - stock_data['Close'].shift())

        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        atr = true_range.rolling(window=window).mean()
        stock_data['ATR'] = atr
        return stock_data
    def calculate_vwap(self, stock_data):
        q = stock_data['Volume'] * stock_data['Close']
        vwap = q.cumsum() / stock_data['Volume'].cumsum()
        stock_data['VWAP'] = vwap
        return stock_data
    def calculate_historical_volatility(self, stock_data, window=30):
        log_returns = np.log(stock_data['Close'] / stock_data['Close'].shift(1))
        volatility = log_returns.rolling(window=window).std() * np.sqrt(252)  # annualize the volatility
        stock_data['Volatility'] = volatility
        return stock_data