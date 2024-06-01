# Algorithmic Trading Bot

## Overview
This project involves the development of an algorithmic trading bot using Python and the CCXT library for interacting with the Binance exchange. The bot implements a moving average crossover strategy to generate buy and sell signals based on historical price data of cryptocurrencies.

## Features
- Fetches historical OHLCV data from the Binance exchange.
- Implements a moving average crossover strategy to generate trading signals.
- Executes buy and sell orders based on the generated signals.
- Continuous monitoring and execution of trades in real-time.
- Provides visualizations of price data and trading signals.

## Setup
1. Install dependencies:
pip install ccxt pandas numpy matplotlib


2. Set up Binance API keys:
- Obtain API key and secret from Binance.
- Set `api_key` and `api_secret` variables in the code.

3. Run the trading bot:
python trading_bot.py


## Usage
- Customize parameters such as trading symbol, timeframe, and moving average windows as needed.
- Modify or add additional trading strategies to enhance performance.
- Implement error handling and logging for robustness in production environments.
