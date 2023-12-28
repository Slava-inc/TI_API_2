import tinkoff.invest as ti
import pandas as pd
import id.basek
import id.accid
import os
from pathlib import Path

# print(os.popen("dir").read())

class Portfolio():
    def __init__(self, token, id):
        self.token = token
        self.id = id

        self.positions = {}
        self.positions['figi'] = []
        self.positions['position'] = []
        self.data = {}
        self.data['figi'] = []
        self.data['instrument'] = []
        self.data['position'] = []
        
        self.result = {}
        
    def set_portfolio(self):
        SDK = ti.Client(self.token)
        with SDK as client:
            self.portfolio = client.operations.get_portfolio(account_id=self.id)

        for position in self.portfolio.positions:
            self.positions['figi'].append(position.figi)
            self.positions['position'].append(position)
            
    def create(self):
        self.set_portfolio()
        SDK = ti.Client(self.token)
        with SDK as client:
            etfs = client.instruments.etfs(instrument_status=2).instruments
            curs = client.instruments.currencies(instrument_status=2).instruments
            shares = client.instruments.shares(instrument_status=2).instruments
            
        for instr in etfs:
            for index in range(len(self.positions['figi'])):
                if instr.figi == self.positions['figi'][index]:
                    self.data['figi'].append(instr.figi)
                    self.data['position'].append(self.positions['position'][index])
                    self.data['instrument'].append(instr)
            
             
        for instr in curs:
            for index in range(len(self.positions['figi'])):
                if instr.figi == self.positions['figi'][index]:
                    self.data['figi'].append(instr.figi)
                    self.data['position'].append(self.positions['position'][index])
                    self.data['instrument'].append(instr)
                    
        for instr in shares:
            for index in range(len(self.positions['figi'])):
                if instr.figi == self.positions['figi'][index]:
                    self.data['figi'].append(instr.figi)
                    self.data['position'].append(self.positions['position'][index])
                    self.data['instrument'].append(instr)
    
    def get_columns(self):
        header = []
        for keys, values in self.result.items():
            for col in values:
                header.append(col)
        return header
                            
    def print(self):
        info = self.get_info()
        
        header = self.get_columns()
        columns = ''
        for col in header:
            columns += ' ' + col
        print(columns)            
            
        i = len(info[0])
        for item in range(i):
            result = ''
            for pos in range(len(info)):
                result += ' ' + info[pos][item]
            print(result)
                
    def get_info(self):
        info = []
        for keys, values in self.result.items():
            for value in values:
                info.append([getattr(mem, value) for mem in self.data[keys]])
        return info
    
    def save_info(self, filename):
        if len(self.result) > 0:
            info = self.get_info()
        elif len(self.data.figi) == 0:
            print('empty info data')
            return
        
        columns = self.get_columns()
        df_dict = {}
        for col in columns:
            df_dict[col] = []
            
        info = self.get_info()        
        i = len(info[0])
        for item in range(i):
            for pos in range(len(info)):
                df_dict[columns[pos]].append(info[pos][item])
        filepath = Path('csv_files/' + filename)
        try:
            pd.DataFrame(df_dict).to_csv(filepath)
            print('file''s saved')
        except OSError as err:
            print("OS error:", err)
            
            
        
        
        
            
        