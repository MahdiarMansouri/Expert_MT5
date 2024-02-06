import MetaTrader5 as mt5
from datetime import datetime
import time
import numpy as np


class StrategyValidator:
    def __init__(self, last_n_bars, timeframe, symbol):
        self.last_n_bar = last_n_bars
        self.timeframe = timeframe
        self.symbol = symbol

    def pinbar_finder(self):
        # finding last closed bar
        last_closed_bar = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 1, 1)

        # Defining direction of bar
        last_candle_color = 'green' if last_closed_bar['close'] - last_closed_bar['open'] > 0 else 'red'
        print(f'   Last Closed bar: {last_closed_bar} \n   and last closed bar color: {last_candle_color}')

        # Defining values of bar parts (body, shadow up, shadow down)
        body = np.abs(last_closed_bar['close'] - last_closed_bar['open'])

        if last_candle_color == 'green':
            shadow_up = last_closed_bar['high'] - last_closed_bar['close']
            shadow_down = last_closed_bar['open'] - last_closed_bar['low']
        else:
            shadow_up = last_closed_bar['high'] - last_closed_bar['open']
            shadow_down = last_closed_bar['close'] - last_closed_bar['low']

        print(f'shadow up => {shadow_up[0]:.4f}')
        print(f'shadow down => {shadow_down[0]:.4f}')
        print(f'body => {body[0]:.4f}')

        if shadow_up[0] > body[0] or shadow_down[0] > body[0]:
            self.pin_bar = last_closed_bar

            # Request the last n bars
            bars = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, self.last_n_bar)

            # Display the bars
            for bar in bars:
                # Convert time in seconds to the datetime format
                time_ = datetime.fromtimestamp(bar['time'])
                candle_color = 'green' if bar['close'] - bar['open'] > 0 else 'red'
                print(
                    f"Time: {time_}, Open: {bar['open']}, High: {bar['high']}, Low: {bar['low']}, "
                    f"Close: {bar['close']}, Color: {candle_color}")

            # Defining last n candles trend
            candles_close_mean = np.mean(bars['close'])
            if candles_close_mean > bars['close'][-1]:
                self.trend = 'down'
                # Check the valid pin bar against trend
                if (shadow_down / 3) > shadow_up:
                    comment = 'Last {} Bars Trend: {}, PinBar: {}'.format(str(self.last_n_bar), self.trend, 'Correct')
                    return comment, 1, self.trend
                else:
                    comment = 'Last {} Bars Trend: {}, PinBar: {}'.format(str(self.last_n_bar), self.trend, 'Incorrect')
                    return comment, 0, self.trend
            else:
                self.trend = 'up'
                if (shadow_up / 3) > shadow_down:
                    comment = 'Last {} Bars Trend: {}, PinBar: {}'.format(str(self.last_n_bar), self.trend, 'Correct')
                    return comment, 1, self.trend
                else:
                    comment = 'Last {} Bars Trend: {}, PinBar: {}'.format(str(self.last_n_bar), self.trend, 'Incorrect')
                    return comment, 0, self.trend
        else:
            comment = 'Its not PinBar...'
            return comment, 0, 'no trend..'

    def pinbar_validator(self):
        # check when the new candle (validator bar) is closed and our pinbar go to the third position in chart
        print('... Waiting for validator bar ... ')
        counter = 1
        while True:
            time.sleep(1)
            print(counter)
            last_2_bar = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 2, 1)
            if self.pin_bar == last_2_bar:
                validator_bar = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 1, 1)
                if self.trend == 'down':
                    if validator_bar['close'] > self.pin_bar['close']:
                        comment = 'PinBar is Valid!  :) '
                        return comment, validator_bar, self.pin_bar, 1
                    else:
                        comment = 'Unfortunately, PinBar is Invalid...  :( '
                        return comment, 0, 0, 0
                else:
                    if validator_bar['close'] < self.pin_bar['close']:
                        comment = 'PinBar is Valid!  :) '
                        return comment, validator_bar, self.pin_bar, 1
                    else:
                        comment = 'Unfortunately, PinBar is Invalid...  :( '
                        return comment, 0, 0, 0
            counter += 1
