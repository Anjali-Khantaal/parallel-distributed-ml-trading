import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Strategy Logic Using Model Predictions
class ModelBasedStrategy(bt.Strategy):
    def __init__(self, model):
        self.data_close = self.datas[0].close
        self.model = model

    def next(self):
        # Prepare features for the model
        lookback = 8  # Change to match model expectation
        if len(self.data_close) < lookback:
            return  # Not enough data for the lookback window

        # Extract recent prices for the lookback window
        features = np.array(self.data_close.get(size=lookback)).reshape(1, -1)

        # Ensure feature names match the model's expectations
        features = pd.DataFrame(features, columns=["SMA_20", "EMA_20", "RSI", "RSI_SMA_Ratio", "Volatility", "Close_lag_1", "Close_lag_2", "Momentum"])

        # Make prediction
        prediction = self.model.predict(features)[0]
        # print(f"Prediction: {prediction}, Features: {features.values}")

        # Trading Logic: Buy if prediction is 1 (price up), Sell if 0 (price down)
        if prediction == 1 and not self.position:
            print("Executing BUY order")
            self.buy()
        elif prediction == 0 and self.position:
            print("Executing SELL order")
            self.sell()

# Backtesting Function
def run_backtest(data, model, cash=10000):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(ModelBasedStrategy, model=model)

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    cerebro.broker.setcash(cash)
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

    results = cerebro.run()
    sharpe_ratio = results[0].analyzers.sharpe.get_analysis()
    drawdown = results[0].analyzers.drawdown.get_analysis()

    return {
        'final_value': cerebro.broker.getvalue(),
        'sharpe_ratio': sharpe_ratio.get('sharperatio', None),
        'max_drawdown': drawdown.max.drawdown
    }

# Visualization Function
def plot_equity_curve(results):
    equity_curves = [result['final_value'] for result in results]
    tickers = [result['ticker'] for result in results]
    plt.figure(figsize=(10, 6))
    plt.bar(tickers, equity_curves, color='skyblue')
    plt.title('Equity Curve')
    plt.xlabel('Ticker')
    plt.ylabel('Final Portfolio Value')
    plt.show()

# Example Data Loading
def load_data(file_path):
    data = pd.read_csv(file_path, header=0, 
                   skiprows=[1, 2], parse_dates=["Price"])
    data = data.rename(columns={
        'Price': 'Date',
        'Adj Close': 'close',
        'Volume': 'volume'
    })
    # Ensure the 'Date' column is converted to datetime and set as index
    if 'Date' in data.columns:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
        data = data.set_index('Date')
    
    # Drop rows with missing or invalid dates
    data = data.dropna()  # Drop based on 'close' to ensure valid data rows remain

    return data