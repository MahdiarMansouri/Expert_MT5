import MetaTrader5 as mt5
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

# prepare the buy request structure
symbol = 'XAUUSD.ecn'

symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()
# print(symbol_info)

# if the symbol is unavailable in MarketWatch, add it
if not symbol_info.visible:
    print(symbol, "is not visible, trying to switch on")
    if not mt5.symbol_select(symbol, True):
        print("symbol_select({}}) failed, exit", symbol)
        mt5.shutdown()
        quit()

lot = 0.01
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

# Define strategy for opening a trade
def should_open_trade():
    # Implement your trading strategy logic here
    # For example, checking some indicators, market conditions, etc.
    return True

# Check if the strategy conditions are met
if should_open_trade():
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
        print("Order successfully placed!")

# Shutdown the MT5 connection
mt5.shutdown()
