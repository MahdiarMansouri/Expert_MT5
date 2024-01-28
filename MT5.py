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
symbol = 'EURUSD'
lot = 0.01


symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(symbol, "not found, can not call order_check()")
    mt5.shutdown()
    quit()

# Define strategy for opening a trade
def should_open_trade():
    # Implement your trading strategy logic here
    # For example, checking some indicators, market conditions, etc.
    return True

# Main trading loop
while True:
    # Check if the strategy conditions are met
    if should_open_trade():
        # Define request structure for trade
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol),
            "sl": 0,  # Stop loss
            "tp": 0,  # Take profit
            "deviation": 20,
            "magic": 234000,
            "comment": "Python script trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # Send trade request
        result = mt5.order_send(request)
        if result != mt5.TRADE_RETCODE_DONE:
            print("Failed to send order :(", result)
        else:
            print("Order successfully placed!")

    # Sleep for a while before the next iteration
    time.sleep(60)  # Sleep for 60 seconds

# Shutdown the MT5 connection
mt5.shutdown()
