import tkinter as tk
from tkinter import Tk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import mplfinance as fplt
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timezone
import ast

import sys
import os
sys.path.append(os.path.dirname(__file__)+ "/..")
if __package__:
    from .lib.candles import Candles
else:
    from lib.candles import Candles
import tinkoff.invest as ti
import id.basek
import id.accid
import Pmw
from Get_Futures_Shares_List import Futures

TOKEN = id.basek.TINKOFF_INVEST_ALL
SDK = ti.Client(TOKEN)
User_acc_ID = id.accid.ACC_ID

candles = Candles(TOKEN, User_acc_ID)

# tf = ti.CandleInterval.CANDLE_INTERVAL_DAY
tf = ti.CandleInterval.CANDLE_INTERVAL_4_HOUR
start_date = datetime(2023, 12, 12, 0, tzinfo=timezone.utc)
end_date = datetime(2024, 1, 10, 19, 0, tzinfo=timezone.utc)
# figi = 'FUTCNYRUBF00' # 'BBG00M0C8YM7'

chosen_future = Futures()
futures_names = chosen_future.df_futures.name
default_feature = futures_names[593]

root = Tk()

root.title("Terminal")
root.geometry('1000x800')

# futures combobox
choice = None
def choseEntry(entry):
    chosen_future.future_name = entry
    chosen_future.set_figi(entry)
    choice.configure(text=chosen_future.get_info()) # filling label choice
    # print('You chose {}, figi = {}'.format(entry, chosen_future.future_figi))    

combobox = Pmw.ComboBox(root, label_text='Futures:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        selectioncommand=choseEntry,
                        scrolledlist_items=futures_names)
combobox.grid(column= 0, row=0, sticky = 'w', padx=8, pady=8)
combobox.selectitem(default_feature)
 
choice = Label(root, text='futures', relief='sunken', padx=20, pady=10, justify='left')
choice.grid(column=0, row=1, sticky='w', padx=8, pady=8)
choseEntry(default_feature) 

def buttonPress(btn):
    
    interval = ti.CandleInterval.CANDLE_INTERVAL_DAY
    match btn:
        case '1M':
            print('The button was pressed 1M')
            interval = ti.CandleInterval.CANDLE_INTERVAL_1_MIN
        case '5M':
            print('The button was pressed 5M')
            interval = ti.CandleInterval.CANDLE_INTERVAL_5_MIN   
        case '10M':
            print('The button was pressed 10M')
            interval = ti.CandleInterval.CANDLE_INTERVAL_10_MIN   
        case '1Ч':
            print('The button was pressed 1Ч')
            interval = ti.CandleInterval.CANDLE_INTERVAL_HOUR
        case '4Ч':
            print('The button was pressed 4Ч')   
            interval = ti.CandleInterval.CANDLE_INTERVAL_4_HOUR
        case 'Д':
            print('The button was pressed Д')   
            interval = ti.CandleInterval.CANDLE_INTERVAL_DAY
        case 'Мес':
            print('The button was pressed Мес')
            interval = ti.CandleInterval.CANDLE_INTERVAL_MONTH
        case 'Индикаторы':
            print('The button was pressed Индикаторы')   
    if btn == 'Индикаторы':
        return btn
    else:
        candles.create(start_date=start_date, end_date=end_date, interval=interval, figi=chosen_future.future_figi)
        candles.get_all_candles_from_cache()
        candles.get_drawing(chosen_future.future_figi)
        canvas.draw()
        # return fig        


                 
def defaultKey(event):
    intervalBox.invoke()
   
intervalBox = Pmw.ButtonBox(root, labelpos='nw', label_text='', padx=0)
intervalBox.add('1M', command = lambda b='1M': buttonPress(b))
intervalBox.add('5M', command = lambda b='5M': buttonPress(b))
intervalBox.add('10M', command = lambda b='10M': buttonPress(b))
intervalBox.add('1Ч', command = lambda b='1Ч': buttonPress(b))
intervalBox.add('4Ч', command = lambda b='4Ч': buttonPress(b))
intervalBox.add('Д', command = lambda b='Д': buttonPress(b))
intervalBox.add('Mес', command = lambda b='Мес': buttonPress(b))
intervalBox.add('Индикаторы', command = lambda b='Индикаторы': buttonPress(b))
intervalBox.setdefault('Д')
root.bind('<Return>', defaultKey)
root.focus_set()
intervalBox.alignbuttons()
intervalBox.grid(column=0, row=2, sticky='w')

menu_bar = Menu(root)  # menu begins
file_menu = Menu(menu_bar, tearoff=0)
# all file menu-items will be added here next
menu_bar.add_cascade(label='File', menu=file_menu)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
view_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='View', menu=view_menu)
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menu_bar)  # menu ends

candles.create(start_date=start_date, end_date=end_date, interval=tf, figi=chosen_future.future_figi, futures=True)
candles.get_all_candles_from_cache()
fig = candles.get_drawing(chosen_future.future_figi)

canvas = FigureCanvasTkAgg(fig, root)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=3)
	
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=0, row=4, sticky='w')
root.mainloop()