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

while True:
    vbar = mt5.copy_rates_from_pos(symbol, timeframe, 1, 1)
    pbar = mt5.copy_rates_from_pos(symbol, timeframe, 2, 1)
    st = SetOrders(vbar, pbar, symbol, lot, timeframe)
    r = st.set_buy_order()
    # print(r)
    print(st.check_order(r))
    time.sleep(5)

# Shutdown the MT5 connection
mt5.shutdown()
