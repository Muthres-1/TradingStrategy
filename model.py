import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
from joblib import dump, load
from indicators import calculate_indicators, add_lagged_features

def predict_for_company(model, ticker):
    df = yf.download(ticker)
    
    if df.empty:
        print(f"No data fetched for {ticker}.")
        return None
    
    print(f"Fetched data for {ticker}:\n{df.tail()}")
    df = calculate_indicators(df)
    df = add_lagged_features(df)

    last_data = df.iloc[-1][['Close_Lag_1', 'RSI_Lag_1', 'MACD_Lag_1', 'ATR_Lag_1', 'Momentum_Lag_1', '%K_Lag_1', '%D_Lag_1']].values
    prediction = model.predict([last_data])
    return prediction[0]

def train_model(data):
    X = data.drop(columns=['Close', 'Ticker'])
    y = data['Close'].shift(-1).dropna()  # Predict the next day's closing price
    X = X.loc[y.index]  # Align X with y
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Model trained with MSE: {mse}")

    return model

def save_model(model, filename='stock_model.joblib'):
    dump(model, filename)

def load_model(filename='stock_model.joblib'):
    return load(filename)
