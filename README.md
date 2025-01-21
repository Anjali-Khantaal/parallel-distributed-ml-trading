# Overview

This project demonstrates a minimal end-to-end algorithmic trading pipeline, leveraging distributed computing to enhance data processing and model training. It covers data preparation, distributed machine learning, and backtesting to evaluate trading strategies.

## Features

- Data Preparation: Clean historical market data and generate technical indicators.
- Distributed Training: Use Dask to parallelize training of machine learning models like Random Forest.
- Backtesting: Simulate trades and evaluate performance using metrics such as Sharpe ratio and maximum drawdown.
- Modular Design: Easily extendable codebase for exploring new strategies.

## Steps to Run

- Install all the dependencies from requirements.txt
- Prepare Data: Process historical data with data_preparation.ipynb
- Train Model: Train models in parallel using distributed_training.ipynb
- Backtest: Evaluate strategy performance in backtesting_and_evaluation.ipynb

## Highlights

- Demonstrates distributed computing with Dask to handle large datasets efficiently.
- Offers a hands-on introduction to algorithmic trading workflows.

## Future Work

- Add real-time trading capabilities.
- Explore advanced models and portfolio optimization.

## License

Licensed under MIT—feel free to use and modify with attribution.
