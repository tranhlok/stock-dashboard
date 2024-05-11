import plotly.graph_objs as go

class StockVisualizer:
    def plot_moving_averages(self, stock_data):
        ma_fig = go.Figure()
        ma_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], name='Close', mode='lines'))
        for window in [20, 50, 200]:
            ma_fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data[f'SMA_{window}'],
                name=f'SMA {window}',
                mode='lines'
            ))
            ma_fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data[f'EMA_{window}'],
                name=f'EMA {window}',
                mode='lines',
                line=dict(dash='dot')
            ))
        return ma_fig

    def plot_candlestick(self, stock_data, symbol, time_range):
        candlestick_chart = go.Figure(data=[
            go.Candlestick(
                x=stock_data.index,
                open=stock_data['Open'],
                high=stock_data['High'],
                low=stock_data['Low'],
                close=stock_data['Close']
            )
        ])
        candlestick_chart.update_layout(
            title=f"{symbol} Candlestick Chart ({time_range})",
            xaxis_rangeslider_visible=False
        )
        return candlestick_chart

    def plot_bollinger_bands(self, stock_data):
        bb_fig = go.Figure()
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Bollinger High'], fill=None, mode='lines', name='Bollinger High'))
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], fill='tonexty', mode='lines', name='Close'))
        bb_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Bollinger Low'], fill='tonexty', mode='lines', name='Bollinger Low'))
        return bb_fig

    def plot_obv(self, stock_data):
        obv_fig = go.Figure()
        obv_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['OBV'], mode='lines', name='OBV'))
        return obv_fig

    def plot_rsi(self, stock_data):
        rsi_fig = go.Figure()
        rsi_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], name='RSI'))
        rsi_fig.update_layout(title="Relative Strength Index (RSI)", xaxis_title="Date", yaxis_title="RSI")
        return rsi_fig

    def plot_macd(self, stock_data):
        macd_fig = go.Figure()
        macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], name='MACD Line'))
        macd_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Signal_Line'], name='Signal Line'))
        macd_fig.update_layout(title="Moving Average Convergence Divergence (MACD)", xaxis_title="Date", yaxis_title="MACD")
        return macd_fig

    def plot_atr(self, stock_data):
        atr_fig = go.Figure()
        atr_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['ATR'], name='ATR'))
        atr_fig.update_layout(title="Average True Range (ATR)", xaxis_title="Date", yaxis_title="ATR")
        return atr_fig

    def plot_vwap(self, stock_data):
        vwap_fig = go.Figure()
        vwap_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['VWAP'], name='VWAP', line=dict(color='purple')))
        vwap_fig.update_layout(title="Volume Weighted Average Price (VWAP)", xaxis_title="Date", yaxis_title="VWAP")
        return vwap_fig

    def plot_volatility(self, stock_data):
        vol_fig = go.Figure()
        vol_fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Volatility'], name='Volatility'))
        vol_fig.update_layout(title="Historical Volatility", xaxis_title="Date", yaxis_title="Volatility")
        return vol_fig
    # Additional plotting methods
