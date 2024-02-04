import MetaTrader5 as mt5
from strategy import strategy
import time

# Configure your MT5 account details
account_number = 516701  # Replace with your account number
password = 'p&X7pbw#AFyK'           # Replace with your password
server = 'OtetGroup-MT5'               # Replace with your server
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
lot = 1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

# Strategy params
count = 10
timeframe = mt5.TIMEFRAME_M1

# Define strategy for sending order
while True:
    pin_bar_validation = strategy(count, timeframe, symbol)
    print(f'PinBar Validation: {pin_bar_validation}')

    # Check if the strategy conditions are Ture
    if pin_bar_validation:
        # Define request structure for trade
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": price - 100 * point,  # Stop loss
            "tp": price + 100 * point,  # Take profit
            "deviation": deviation,
            "magic": 234000,
            "comment": "Python script trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }

        # send a trading request
        result = mt5.order_send(request)
        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol, lot, price, deviation))
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            print("shutdown() and quit")
            mt5.shutdown()
            quit()
        else:
            print("Order successfully placed!", end='\n\n')
            print('=' * 20)
    else:
        print('-' * 10)

    time.sleep(60)

# Shutdown the MT5 connection
mt5.shutdown()
