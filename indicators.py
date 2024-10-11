import pandas as pd

def calculate_macd(data):
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def calculate_atr(df, period=14):
    df['High_Low'] = df['High'] - df['Low']
    df['High_Close'] = (df['High'] - df['Close'].shift(1)).abs()
    df['Low_Close'] = (df['Low'] - df['Close'].shift(1)).abs()
    df['True_Range'] = df[['High_Low', 'High_Close', 'Low_Close']].max(axis=1)
    df['ATR'] = df['True_Range'].rolling(window=period).mean()
    df.drop(columns=['High_Low', 'High_Close', 'Low_Close', 'True_Range'], inplace=True)
    return df

def calculate_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

def calculate_stochastic_oscillator(df, k_period=14, d_period=3):
    df['Lowest_Low'] = df['Low'].rolling(window=k_period).min()
    df['Highest_High'] = df['High'].rolling(window=k_period).max()
    df['%K'] = 100 * ((df['Close'] - df['Lowest_Low']) / (df['Highest_High'] - df['Lowest_Low']))
    df['%D'] = df['%K'].rolling(window=d_period).mean()
    df.drop(columns=['Lowest_Low', 'Highest_High'], inplace=True)

def calculate_indicators(df):
    df = calculate_atr(df)
    calculate_rsi(df)
    calculate_stochastic_oscillator(df)

    df['20_MA'] = df['Close'].rolling(window=20).mean()
    df['50_MA'] = df['Close'].rolling(window=50).mean()

    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['BB_Upper'] = df['20_MA'] + (df['Close'].rolling(window=20).std() * 2)
    df['BB_Lower'] = df['20_MA'] - (df['Close'].rolling(window=20).std() * 2)

    df['Momentum'] = df['Close'].diff(4)

    df.dropna(inplace=True)
    return df

def add_lagged_features(df, lags=1):
    for lag in range(1, lags + 1):
        df[f'Close_Lag_{lag}'] = df['Close'].shift(lag)
        df[f'RSI_Lag_{lag}'] = df['RSI'].shift(lag)
        df[f'MACD_Lag_{lag}'] = df['MACD'].shift(lag)
        df[f'ATR_Lag_{lag}'] = df['ATR'].shift(lag)
        df[f'Momentum_Lag_{lag}'] = df['Momentum'].shift(lag)
        df[f'%K_Lag_{lag}'] = df['%K'].shift(lag)
        df[f'%D_Lag_{lag}'] = df['%D'].shift(lag)
    df.dropna(inplace=True)
    return df
