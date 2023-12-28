import tinkoff.invest as ti
import pandas as pd
import id.basek
import id.accid
import os

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
        # columns = ['figi', 'ticker', 'name', 'instrument_type']
        # self.df = pd.DataFrame(columns=columns)
        
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
                    
    def print(self, kw):
        info = self.get_info(kw)
        i = len(info[0])
        for item in range(i):
            result = ''
            for pos in range(len(info)):
                result += ' ' + info[pos][item]
            print(result)
                
    def get_info(self, kw):
        info = []
        for keys, values in kw.items():
            for value in values:
                info.append([getattr(mem, value) for mem in self.data[keys]])
        return info