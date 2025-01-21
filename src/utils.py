import pandas as pd
import dask.dataframe as dd

def process_all_tickers(data_dir="data", output_dir="processed_data"):
    """
    Apply feature engineering to all CSV files in the directory using Dask.

    Parameters:
        data_dir (str): Directory containing raw CSV files.
        output_dir (str): Directory to save processed data.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    for file in os.listdir(data_dir):
        if file.endswith(".csv"):
            df = dd.read_csv(os.path.join(data_dir, file), header=0, 
                   skiprows=[1, 2])
            df = df.map_partitions(compute_technical_indicators)
            output_file = os.path.join(output_dir, file)
            df.to_csv(output_file, single_file=True)
            print(f"Processed and saved: {output_file}")

def compute_technical_indicators(df):
    """
    Compute technical indicators (SMA, EMA, RSI, Bollinger Bands).

    Parameters:
        df (pd.DataFrame): Input data with 'Close' prices.

    Returns:
        pd.DataFrame: Data with added technical indicators.
    """
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["RSI"] = compute_rsi(df["Close"])
    df["Bollinger_Upper"] = df["SMA_20"] + 2 * df["Close"].rolling(window=20).std()
    df["Bollinger_Lower"] = df["SMA_20"] - 2 * df["Close"].rolling(window=20).std()
    df['10_day_MA'] = df['Close'].rolling(window=10).mean()
    df['50_day_MA'] = df['Close'].rolling(window=50).mean()
    df["RSI_SMA_Ratio"] = df["RSI"] / df["SMA_20"]
    df["Volatility"] = df["Close"].rolling(window=20).std()
    df["Close_lag_1"] = df["Close"].shift(1)
    df["Close_lag_2"] = df["Close"].shift(2)
    df["Momentum"] = df["Close"].diff(periods=5)
    return df

def compute_rsi(series, window=14):
    """
    Compute Relative Strength Index (RSI).

    Parameters:
        series (pd.Series): Price series.
        window (int): Window for RSI calculation.

    Returns:
        pd.Series: RSI values.
    """
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
