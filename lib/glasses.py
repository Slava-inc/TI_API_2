import tinkoff.invest as ti
import pandas as pd
import id.basek
import id.accid
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas_ta as ta
import time

# GetOrderBook
class Glass():
    def __init__(self, token, id):
        self.token = token
        self.id = id
        
    def get_glasses(self):
        SDK_client = ti.Client(self.token)
        try:
            with SDK_client as client:        
                glass = client.market_data.get_order_book()
        except ti.invest.RequestError as e:
            print(str(e))