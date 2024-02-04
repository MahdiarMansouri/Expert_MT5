import MetaTrader5 as mt5


class SetOrders:
    def __init__(self, symbol, lot, timeframe):
        self.symbol = symbol
        self.lot = lot
        self.timeframe = timeframe
        self.buy_price = mt5.symbol_info(symbol).ask
        self.sell_price = mt5.symbol_info(symbol).bid
        self.point = mt5.symbol_info(symbol).point
        self.action = mt5.TRADE_ACTION_DEAL
        self.type_time = mt5.ORDER_TIME_GTC
        self.type_filling = mt5.ORDER_FILLING_FOK
        self.deviation = 20
        self.magic = 234000

        # Create request for order
        self.request = {
            "action": self.action,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": None,
            "price": None,
            "sl": None,
            "tp": None,
            "deviation": self.deviation,
            "magic": self.magic,
            "comment": "Python Expert Trade",
            "type_time": self.type_time,
            "type_filling": self.type_filling,
        }

    def set_buy_order(self):
        order_type = mt5.ORDER_TYPE_BUY
        tp = self.buy_price + 100 * self.point
        sl = self.buy_price - 100 * self.point
        self.request['type'] = order_type
        self.request['price'] = self.buy_price
        self.request['sl'] = sl
        self.request['tp'] = tp

        # Define request structure for trade
        request = {
            "action": self.action,
            "symbol": self.symbol,
            "volume": self.lot,
            "type": order_type,
            "price": self.buy_price,
            "sl": sl,
            "tp": tp,
            "deviation": self.deviation,
            "magic": self.magic,
            "comment": "Python Expert Trade",
            "type_time": self.type_time,
            "type_filling": self.type_filling,
        }
