import tinkoff.invest as ti
import pandas as pd
import id.basek
import id.accid
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
import pandas_ta as ta
import time

from tinkoff.invest.utils import now
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.caching.market_data_cache.cache import MarketDataCache
from tinkoff.invest.caching.market_data_cache.cache_settings import (
    MarketDataCacheSettings,)
from tinkoff.invest.caching.market_data_cache.instrument_market_data_storage import (
    InstrumentMarketDataStorage,
)
from tinkoff.invest.caching.market_data_cache.datetime_range import DatetimeRange
import ast
import mplfinance as fplt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#TO DO
# - file name for minutes
# - do with complete = false
# - indicators

class Candles():
    def __init__(self, token, id):
        self.token = token
        self.id = id
        self.fig = None
        self.candle_file = None
        
    def quotation_count(self, quot):
        return quot['units'] + quot['nano'] / 1e9
            
    def create(self, start_date, end_date, interval, figi, futures=False, base_cache_dir="market_data_cache"):
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.figi = figi
        self.base_cache_dir = base_cache_dir
        self.end_hour = 7
        self.start_hour = 0
        hour_interval = [ti.CandleInterval.CANDLE_INTERVAL_HOUR, ti.CandleInterval.CANDLE_INTERVAL_4_HOUR]
        if interval in hour_interval:
            self.end_hour = 15
        if futures:
            self.end_hour = 16
            self.start_hour = 4            
            

        # return self.create_candle_df   
     
    def get_all_candles_from_cache(self):
        with Client(self.token) as client:
            settings = MarketDataCacheSettings(base_cache_dir=Path(self.base_cache_dir))
            market_data_cache = MarketDataCache(settings=settings, services=client)
            # storage = market_data_cache._get_figi_cache_storage(self.figi, self.interval)
            candles = market_data_cache.get_all_candles(
            figi=self.figi,
            from_=self.start_date,
            to=self.end_date,
            interval=self.interval,
            )
            min_date = self.end_date
            max_date = self.start_date
            for candle in candles:
                min_date = min(min_date, candle.time)
                max_date = max(max_date, candle.time)
                # print(candle.time, candle.is_complete)
            self.start_date = min_date
            self.end_date = max_date
            # [_ for _ in candles]
    
    def get_candle_path(self):
        file_name = Path(self.base_cache_dir) / self.figi / self.interval.name
        start_str = str(int(self.start_date.replace(hour=self.start_hour, minute=0, second=0).timestamp()))
        end_str = str(int(self.end_date.replace(hour=self.end_hour, minute=0, second=0).timestamp()))
        self.candle_file = ('./' + str(file_name) + f"-{start_str}-{end_str}.csv").replace('\\', '/')
        return self.candle_file
        
    def create_candle_df(self, candle_path = None):
        if candle_path == None:
            candle_path = self.get_candle_path()
            
        self.df = pd.read_csv(candle_path)
        for column in self.df.columns:
            if column == 'time':
                continue
            self.df[column] = self.df[column].apply(lambda x: self.quotation_count(ast.literal_eval(x)))
            if column == 'close':
                break
    
        self.df['time'] = pd.to_datetime(self.df['time'])
        self.df.set_index('time', inplace=True)      
    
    def get_drawing(self, figi):
        self.create_candle_df()

        # self.fig, _  = fplt.plot(
        #         self.df,
        #         returnfig=True,
        #         type='candle',
        #         style='binancedark',
        #         title='tink candle, style = binancedark',
        #         ylabel='Price ($)',
        #         volume=True,
        #         ylabel_lower='traded',
        #         show_nontrading=True
        #     )
        if self.fig == None:
            self.fig = fplt.figure(style='binancedark')
        ax = self.fig.add_subplot()

        fplt.plot(self.df, ax=ax, type='candle', axtitle='Candle ' + figi)
        return self.fig                        

    def write_candles(self):
        SDK_client = ti.Client(self.token)
        try:
            with SDK_client as client:
                period = datetime.date(self.end_date) - datetime.date(self.start_date)
                period_days = period.days

                for i in range(0, period_days):
                    current_date = self.start_date + timedelta(i)
                    start = [current_date.year, current_date.month, current_date.day, self.start_date.hour, self.start_date.minute]
                    end = [current_date.year, current_date.month, current_date.day, self.end_date.hour, self.end_date.minute]
                    cti_candles = client.market_data.get_candles(
                        figi=self.figi,
                        from_=datetime(start[0], start[1], start[2], start[3], start[4]),
                        to=datetime(end[0], end[1], end[2], end[3], end[4]),
                        interval=self.interval
                    )
                    # Обработка запроса по форме
                    candle_df = self.create_candle_df(cti_candles.candles)
                    if candle_df.empty:
                        continue
                    else:
                        # Добавление индикаторов
                        candle_df['ema'] = ta.ema(candle_df['close'], 10)
                        candle_df['ma'] = ta.sma(candle_df['close'], lenght=10)
                        # Запись полученных данных в табличку
                        # указать название файла соответствующее инструменту
                        filepath = Path('csv_files/' + self.figi + '.csv')
                        df = pd.DataFrame(candle_df)
                        print(df.dtypes)
                        df.to_csv(filepath, mode='a')
                        time.sleep(0.1)
                        print('Record ', i, ' complete')

                df_check = pd.read_csv('csv_files/instrument_name.csv')
                # Убираем пропуски значений
                df_check.dropna(inplace=True)
                # Убираем повторения названий из выгрузки
                df_check.drop_duplicates(subset=['time', 'volume', 'open', 'close', 'high', 'low'],
                                        inplace=True
                                        )
                df_check.drop(columns=['Unnamed: 0'], inplace=True)
                print(df_check.dtypes)
                df = df_check.convert_dtypes(infer_objects=True)
                # Запись полученных данных в табличку
                # указать название файла соответствующее инструменту
                filepath = Path('csv_files/instrument_name.csv')
                print(df.dtypes)
                df.to_csv(filepath, mode='w') 
                
        except ti.invest.RequestError as e:
            print(str(e))       
        