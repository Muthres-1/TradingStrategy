# Stock Data Prediction

This project fetches stock data from Yahoo Finance, calculates various technical indicators, and uses a neural network model to predict future stock closing prices. The results are uploaded to Google Sheets for further analysis.

## Features

- **Stock Data Fetching**: Retrieve historical stock data for multiple companies using `yfinance`.
- **Technical Indicators**: Calculate key indicators like RSI, MACD, Stochastic Oscillator, ATR, and Bollinger Bands.
- **Prediction**: Predict future stock closing prices using a trained neural network model.
- **Google Sheets Integration**: Upload processed data to Google Sheets for easy sharing and access.

## Project Structure

├── data_fetcher.py # Fetch stock data and calculate indicators 
├── indicators.py # Technical indicators calculations 
├── model.py # Model training and predictions 
├── google_sheets.py # Google Sheets interaction 
├── trading_model.joblib # Pre-trained neural network model 
├── matching_companies.csv # Example output with matching companies based on MACD 
├── README.md # This file 
├── requirements.txt # Python dependencies
└── CompaniesSymbols.csv # Input file with stock ticker symbols


## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/stock-data-prediction.git
    cd stock-data-prediction
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google Sheets API:

    - Download the credentials JSON file from Google Cloud.
    - Place it in the project directory and update the file path in the code or use environment variables.

## How to Use

1. **Fetch and Process Stock Data**:

    Use the main function in `data_fetcher.py` to download stock data, calculate technical indicators, and upload it to a Google Sheet.

    ```bash
    python data_fetcher.py
    ```

2. **Predict Future Stock Prices**:

    Run `model.py` to make predictions using the pre-trained neural network model.

    ```bash
    python model.py
    ```

3. **MACD Signal Matching**:

    Find matching companies where the MACD signal is close to the signal line and has increasing volume:

    ```bash
    python find_macd_matches.py
    ```

4. **Model Training (Optional)**:

    You can re-train the neural network model using `train_model_nn()` in `model.py`.

## Google Sheets Integration

To use Google Sheets integration:

1. Enable the Google Sheets API from the Google Cloud Console.
2. Download the credentials JSON file and place it in the project directory.
3. Set the correct file path in the code or manage it with environment variables.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## requirements.txt

Ensure the following dependencies are listed in `requirements.txt`:

