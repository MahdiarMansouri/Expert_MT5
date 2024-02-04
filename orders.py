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

        # send a trading request
        order_result = mt5.order_send(self.request)

        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(self.symbol, self.lot,
                                                                                     self.buy_price, self.deviation))
        return order_result

    def set_sell_order(self):
        order_type = mt5.ORDER_TYPE_SELL
        tp = self.sell_price - 100 * self.point
        sl = self.sell_price + 100 * self.point
        self.request['type'] = order_type
        self.request['price'] = self.buy_price
        self.request['sl'] = sl
        self.request['tp'] = tp

        # send a trading request
        order_result = mt5.order_send(self.request)

        # check the execution result
        print("1. order_send(): by {} {} lots at {} with deviation={} points".format(self.symbol, self.lot,
                                                                                     self.sell_price, self.deviation))
        return order_result

    def check_order(self, result):
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
            return False
        else:
            print("Order successfully placed!", end='\n\n')
            print('=' * 20)
            return True
