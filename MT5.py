import MetaTrader5 as mt5
from strategy import StrategyValidator
from orders import SetOrders
import time

# Configure your MT5 account details
account_number = 516701  # Replace with your account number
password = 'p&X7pbw#AFyK'  # Replace with your password
server = 'OtetGroup-MT5'  # Replace with your server
path = 'C:\Program Files\MetaTrader 5\\terminal64.exe'

# Initialize MT5 connection
account = mt5.initialize(path=path,
                         login=account_number,
                         password=password,
                         server=server,
                         portable=False)

if not account:
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Print account information
account_info = mt5.account_info()
if account_info is not None:
    print(f"Balance: {account_info.balance}, Equity: {account_info.equity}")
    print('_' * 30)

# prepare the buy request structure
symbol = 'XAUUSD.ecn'

symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()
else:
    print(f"Symbol: {symbol}")
    print(f"Minimum volume: {symbol_info.volume_min}")
    print(f"Maximum volume: {symbol_info.volume_max}")
    print(f"Volume step: {symbol_info.volume_step}")
    print('_' * 30)

# if the symbol is unavailable in MarketWatch, add it
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on symbol on your MarketWatch!")
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}) failed, exit", symbol)
        mt5.shutdown()
        quit()

# Order params
lot = 0.1

# Strategy params
last_n_bars = 10
timeframe = mt5.TIMEFRAME_M1

# Define StrategyValidator object
SV = StrategyValidator(last_n_bars, timeframe, symbol)

# Define strategy for sending order
while True:
    comment, situation, trend = SV.pinbar_finder()
    print(f'Comment: {comment}, \nPinBar Correction: {situation}')

    # Check if the strategy conditions are Ture
    if situation == 1:
        # check if the validator bar validate our pinbar
        validator_comment, validator_bar, pin_bar, validation = SV.pinbar_validator()
        print(f'Comment: {validator_comment}, \nPinBar Validation: {validation}')
        if validation == 1:
            set_order = SetOrders(validator_bar, pin_bar, symbol, lot, timeframe)
            # check trend for order type (buy or sell)
            if trend == 'down':
                result = set_order.set_buy_order()
                order_situation = set_order.check_order(result)
            else:
                result = set_order.set_sell_order()
                order_situation = set_order.check_order(result)
            print(f'Order situation: {order_situation}')

    else:
        for i in range(60):
            print(i+1)
            time.sleep(1)

        # time.sleep(60)
    print('_' * 100)


# Shutdown the MT5 connection
# mt5.shutdown()
