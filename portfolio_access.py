import tinkoff.invest
import id.basek
import id.accid
import pandas as pd
from lib.portfolio import Portfolio

TOKEN = id.basek.TINKOFF_INVEST_ALL
SDK = tinkoff.invest.Client(TOKEN)
User_acc_ID = id.accid.ACC_ID

port = Portfolio(TOKEN, User_acc_ID)
port.create()
port.result = {'position': ['figi'],
            'instrument': ['ticker', 'name']}    
port.print()