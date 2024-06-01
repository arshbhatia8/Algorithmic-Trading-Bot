import ccxt
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Binance API keys
api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Initialize Binance exchange
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

# Parameters
symbol = 'BTC/USDT'
timeframe = '1h'
short_window = 50
long_window = 200

def fetch_data(symbol, timeframe, limit=500):
    """Fetch historical OHLCV data."""
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def moving_average_strategy(df, short_window, long_window):
    """Implement moving average crossover strategy."""
    df['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1).mean()
    df['signal'] = 0
    df['signal'][short_window:] = np.where(df['short_mavg'][short_window:] > df['long_mavg'][short_window:], 1, 0)
    df['positions'] = df['signal'].diff()
    return df

def plot_signals(df):
    """Plot trading signals."""
    plt.figure(figsize=(12, 8))
    plt.plot(df['close'], label='Close Price', alpha=0.5)
    plt.plot(df['short_mavg'], label=f'Short {short_window}-MA', alpha=0.75)
    plt.plot(df['long_mavg'], label=f'Long {long_window}-MA', alpha=0.75)
    plt.plot(df[df['positions'] == 1].index, df['short_mavg'][df['positions'] == 1], '^', markersize=10, color='g', lw=0, label='Buy Signal')
    plt.plot(df[df['positions'] == -1].index, df['short_mavg'][df['positions'] == -1], 'v', markersize=10, color='r', lw=0, label='Sell Signal')
    plt.title(f'{symbol} Price and Trading Signals')
    plt.legend()
    plt.show()

def execute_trade(signal, symbol):
    """Execute a trade based on signal."""
    balance = exchange.fetch_balance()
    usdt_balance = balance['total']['USDT']
    btc_balance = balance['total']['BTC']
    
    if signal == 1 and usdt_balance > 10:  # Buy signal
        order = exchange.create_market_buy_order(symbol, usdt_balance / exchange.fetch_ticker(symbol)['last'])
        print(f'Buy order executed: {order}')
    elif signal == -1 and btc_balance > 0.001:  # Sell signal
        order = exchange.create_market_sell_order(symbol, btc_balance)
        print(f'Sell order executed: {order}')

# Fetch data and apply strategy
data = fetch_data(symbol, timeframe)
data = moving_average_strategy(data, short_window, long_window)
plot_signals(data)

# Run trading bot (simplified for demonstration; consider using event-driven approach for real implementation)
while True:
    try:
        data = fetch_data(symbol, timeframe)
        data = moving_average_strategy(data, short_window, long_window)
        latest_signal = data['positions'].iloc[-1]
        
        if latest_signal != 0:
            execute_trade(latest_signal, symbol)
        
        time.sleep(60)  # Wait for 1 minute before the next iteration
    except Exception as e:
        print(f'Error: {e}')
        time.sleep(60)  # Wait for 1 minute before retrying
