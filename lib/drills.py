import tinkoff.invest as ti
import pandas as pd

class Drills():
    def __init__(self, futures, operation_file, trading_file) -> None:
        self.futures = futures
        self.operation_file = operation_file
        self.trading_file = trading_file
        self.df = pd.DataFrame(columns=['date', 'price'])
        
    def buy(self):
        pass
    
        