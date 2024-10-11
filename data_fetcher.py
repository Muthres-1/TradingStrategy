import yfinance as yf
import pandas as pd

def fetch_stock_data(tickers):
    all_data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        stock_data = stock.history(period="max")
        stock_data = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']]
        stock_data = stock_data.asfreq('D').ffill()

        # Calculating additional technical indicators
        stock_data['RSI'] = compute_rsi(stock_data['Close'])
        stock_data['20_MA'] = stock_data['Close'].rolling(window=20).mean()
        stock_data['BB_Upper'] = stock_data['20_MA'] + (stock_data['Close'].rolling(window=20).std() * 2)
        stock_data['BB_Lower'] = stock_data['20_MA'] - (stock_data['Close'].rolling(window=20).std() * 2)
        stock_data['EMA_12'] = stock_data['Close'].ewm(span=12, adjust=False).mean()
        stock_data['EMA_26'] = stock_data['Close'].ewm(span=26, adjust=False).mean()
        stock_data['MACD'] = stock_data['EMA_12'] - stock_data['EMA_26']
        stock_data['Signal_Line'] = stock_data['MACD'].ewm(span=9, adjust=False).mean()
        stock_data['50_MA'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['200_MA'] = stock_data['Close'].rolling(window=200).mean()
        stock_data['Momentum'] = stock_data['Close'].diff(4)
        stock_data['ATR'] = compute_atr(stock_data)
        stock_data['%K'], stock_data['%D'] = compute_stochastic_oscillator(stock_data)
        stock_data['Williams_%R'] = compute_williams_r(stock_data)

        stock_data['Ticker'] = ticker
        stock_data.reset_index(inplace=True)
        stock_data = stock_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'RSI', '20_MA', 'BB_Upper', 'BB_Lower', 'EMA_12', 'EMA_26', 'MACD', 'Signal_Line', '50_MA', '200_MA', 'Momentum', 'ATR', '%K', '%D', 'Williams_%R', 'Ticker']]

        all_data[ticker] = stock_data

    return all_data

# RSI calculation
def compute_rsi(data, window=14):
    delta = data.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Average True Range calculation
def compute_atr(data, window=14):
    high_low = data['High'] - data['Low']
    high_close = (data['High'] - data['Close'].shift()).abs()
    low_close = (data['Low'] - data['Close'].shift()).abs()

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(window=window).mean()

# Stochastic Oscillator calculation
def compute_stochastic_oscillator(data, k_window=14, d_window=3):
    low_min = data['Low'].rolling(window=k_window).min()
    high_max = data['High'].rolling(window=k_window).max()
    data['%K'] = (data['Close'] - low_min) / (high_max - low_min) * 100
    data['%D'] = data['%K'].rolling(window=d_window).mean()
    return data['%K'], data['%D']

# Williams %R calculation
def compute_williams_r(data, window=14):
    highest_high = data['High'].rolling(window=window).max()
    lowest_low = data['Low'].rolling(window=window).min()
    return -100 * ((highest_high - data['Close']) / (highest_high - lowest_low))
