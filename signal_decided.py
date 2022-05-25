import pandas as pd
from binance.client import Client
import asyncio
from binance import AsyncClient,BinanceSocketManager,ThreadedWebsocketManager
import ta
import numpy as np
import time
import nest_asyncio
nest_asyncio.apply()

import sqlalchemy

from datetime import datetime, timedelta


class Signals:
    
    def __init__(self,symbol,interval,lookback,lags):
        self.symbol = symbol
        self.interval = interval
        self.lookback = lookback
        self.lags = lags
    
    def getminutedata(self):
        
        frame = pd.DataFrame(client.get_historical_klines(self.symbol, self.interval, self.lookback + ' hour ago UTC')) #'min ago UTC' 'day' ya da 'hour' olarakta giriliyor
        frame = frame.iloc[:,:6]
        frame.columns = ['Time','Open','High','Low','Close','Volume']
        frame = frame.set_index('Time')
        frame.index = pd.to_datetime(frame.index, unit='ms')
        frame = frame.astype(float)
        return frame
    
    def applytechnicals(self):
        df = self.getminutedata()
        df['%K'] = ta.momentum.stoch(df.High, df.Low,df.Close, window=14, smooth_window=3)
        df['%D'] = df['%K'].rolling(3).mean()
        df['rsi'] = ta.momentum.rsi(df.Close, window=14)
        df['macd'] = ta.trend.macd_diff(df.Close)
        df['sma_s'] = ta.trend.sma_indicator(df.Close, window=50) #MA(50) için short pozisyon
        df['sma_l'] = ta.trend.sma_indicator(df.Close, window=200) #MA(200) için long pozisyon
        df.dropna(inplace=True)
        return df
        
    def gettrigger(self):
        df = self.applytechnicals()
        dfx = pd.DataFrame()
        for i in range(self.lags + 1):
            mask = (df['%K'].shift(i) < 20) & (df['%D'].shift(i < 20))
            dfx = pd.concat([dfx,mask], axis=1, ignore_index=True)
        return dfx.sum(axis=1)
    def decide(self):
        df = self.applytechnicals()
        df['trigger'] = np.where(self.gettrigger(), 1, 0)
        df['Buy'] = np.where((df.trigger) & (df['%K'].between(20,80)) & (df['%D'].between(20,80)) & (df.rsi > 50) & (df.macd > 0) & (df.sma_s > df.sma_l) & (df.Close > df.sma_s) & (df.Close > df.sma_l) , 1, 0)
        return df[df['Buy'] == 1]


if __name__ == "__main__": 

    #Futures_TestKey
    api_key = "cd7dd6566641573506d773034ce5ef8d30c68053a650e3ff093c5f64fa78b87a"
    secret_key = "17a41707a491780e797ff8c43a2e4e52cfb53fa378248b5b0c12ead6ddf94b53"

    client = Client(api_key = api_key, api_secret = secret_key, tld = "com", testnet = True)   
    
    symbol = 'BTCUSDT'
    interval = '1m'
    lookback = '25'
    lags = 25
    
    buy_signal = Signals(symbol = symbol, interval = interval, lookback = lookback, lags = lags)
    print(buy_signal.decide())







