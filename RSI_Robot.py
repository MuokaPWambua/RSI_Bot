from pprint import pprint
import pandas as pd
import numpy as np
import datetime
from datetime import datetime
from datetime import date
import MetaTrader5 as mt5
import time
from stock_indicators import indicators
from stock_indicators.indicators.common import Quote


# Get the Data
if not mt5.initialize():
    print (f"cant start mt5 error={mt5.last_error}")
    quit()

pair = "EURUSD"
lot = 0.5

pair_info = mt5.symbol_info(pair)
rates = mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_H1, 0, 1000)
df = pd.DataFrame(rates).dropna()
df['date'] = pd.to_datetime(df['time'], unit='s')

# Signal Processing
close = np.array(df['close'])

quotes_list = [
    Quote(d,o,h,l,c,v) 
    for d,o,h,l,c,v 
    in zip(df['date'], df['open'], df['high'], df['low'], df['close'], df['tick_volume'])
]

rsi_ind = indicators.get_rsi(quotes_list, 14)
array_length = len(rsi_ind)
last_element = rsi_ind[- 1]
last_rsi = last_element
array_length3 = len(close)
last_element3 = close[-1]
last_price = last_element3
price = mt5.symbol_info_tick(pair_info)
deviation = 20

#Decission Taking and Send Order
while True:
    if last_rsi.rsi > 70  :
        request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": pair,
                    "volume": lot,
                    "type": mt5.ORDER_TYPE_SELL,
                    "sl": price - 0.002,
                    "tp": price + 0.005,
                    "deviation": deviation,
                    "magic": 202003,
                    "comment": "InUpBot MrEurUsd",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC}
        print('order sent')
        mt5.order_send(request)
                
                
    if 30 > last_rsi.rsi:
        request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": pair,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "sl": price + 0.002,
                "tp": price - 0.005,
                "deviation": deviation,
                "magic": 202003,
                "comment": "InUpBot Lancero",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC}
        print('order sent')
        mt5.order_send(request)
            
    else:
        print('Waiting for Market Signal')