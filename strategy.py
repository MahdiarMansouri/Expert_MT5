import MetaTrader5 as mt5
from datetime import datetime
import time
import numpy as np

# Connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
    quit()

# Define the symbol and timeframe
symbol = "XAUUSD.ecn"
timeframe = mt5.TIMEFRAME_M1  # 1-minute timeframe
count = 10

while True:
    # finding last closed bar
    last_2_bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, 2)
    last_closed_bar = last_2_bars[0]

    # Defining direction of bar
    candle_color = 'green' if last_closed_bar['close'] - last_closed_bar['open'] > 0 else 'red'

    # Defining values of bar parts (body, shadow up, shadow down)
    body = np.abs(last_closed_bar['close'] - last_closed_bar['open'])

    if candle_color == 'green':
        shadow_up = last_closed_bar['high'] - last_closed_bar['close']
        shadow_down = last_closed_bar['open'] - last_closed_bar['low']
    else:
        shadow_up = last_closed_bar['high'] - last_closed_bar['open']
        shadow_down = last_closed_bar['close'] - last_closed_bar['low']

    # Defining pin bar
    pin_bar = None

    if shadow_up or shadow_down > body:
        pin_bar = last_closed_bar

    if pin_bar:
        print('yes')

    exit()

    # Request the last 2 1-minute bars
    bars = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    # print(bars['close'])
    # print(type(bars))

    # Display the bars
    for bar in bars:
        # Convert time in seconds to the datetime format
        time_ = datetime.fromtimestamp(bar['time'])
        candle_color = 'green' if bar['close'] - bar['open'] > 0 else 'red'
        print(
            f"Time: {time_}, Open: {bar['open']}, High: {bar['high']}, Low: {bar['low']}, Close: {bar['close']}, Color: {candle_color}")

    candles_close_mean = np.mean(bars['close'])
    if candles_close_mean > bars['close'][-1]:
        trend = 'down'
    else:
        trend = 'up'



    print(trend)
    print('-' * 50)
    time.sleep(60)

