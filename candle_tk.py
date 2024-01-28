import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import mplfinance as fplt
# import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timezone
import ast

import sys
import os
sys.path.append(os.path.dirname(__file__)+ "/..")
# if __package__:
#     from .lib.candles import Candles
# else:
#     from lib.candles import Candles
from lib.candles import Candles
import tinkoff.invest as ti
import id.basek
import id.accid
import Pmw
from Get_Futures_Shares_List import Futures
from os import listdir
from os.path import isfile, join
from pathlib import Path

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
root.geometry('1000x1200') #1000x800

frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 8])

# futures combobox
choice = None
def choseEntry(entry):
    chosen_future.future_name = entry
    chosen_future.set_figi(entry)
    choice.configure(text=chosen_future.get_info()) # filling label choice
    # print('You chose {}, figi = {}'.format(entry, chosen_future.future_figi))    

combobox = Pmw.ComboBox(frame, label_text='Futures:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        selectioncommand=choseEntry,
                        scrolledlist_items=futures_names)
combobox.grid(column= 0, row=0, sticky = 'w', padx=8, pady=8)
combobox.selectitem(default_feature)
 
choice = Label(frame, text='futures', relief='sunken', padx=20, pady=10, justify='left')
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
   
intervalBox = Pmw.ButtonBox(frame, labelpos='nw', label_text='', padx=0)
intervalBox.add('1M', command = lambda b='1M': buttonPress(b))
intervalBox.add('5M', command = lambda b='5M': buttonPress(b))
intervalBox.add('10M', command = lambda b='10M': buttonPress(b))
intervalBox.add('1Ч', command = lambda b='1Ч': buttonPress(b))
intervalBox.add('4Ч', command = lambda b='4Ч': buttonPress(b))
intervalBox.add('Д', command = lambda b='Д': buttonPress(b))
intervalBox.add('Mес', command = lambda b='Мес': buttonPress(b))
intervalBox.add('Индикаторы', command = lambda b='Индикаторы': buttonPress(b))
intervalBox.setdefault('Д')
frame.bind('<Return>', defaultKey)
frame.focus_set()
intervalBox.alignbuttons()
intervalBox.grid(column=0, row=2, sticky='w')

def candle_options():
    w_option = Tk()
    w_option.title("candle options")
    w_option.geometry("250x200")
    # furtures, start_date, end_date, interval

menu_bar = Menu(frame)  # menu begins
file_menu = Menu(menu_bar, tearoff=0)
# all file menu-items will be added here next
menu_bar.add_cascade(label='File', menu=file_menu)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
view_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='View', menu=view_menu)
option_menu = Menu(menu_bar, tearoff=0)
option_menu.add_command(label='candles', command=candle_options)
menu_bar.add_cascade(label='Options',  menu=option_menu)
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menu_bar)  # menu ends

candles.create(start_date=start_date, end_date=end_date, interval=tf, figi=chosen_future.future_figi, futures=True)
candles.get_all_candles_from_cache()
fig = candles.get_drawing(chosen_future.future_figi)

canvas = FigureCanvasTkAgg(fig, frame)
canvas.draw()
canvas.get_tk_widget().grid(column=0, row=3)
	
toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar=False)
toolbar.update()
toolbar.grid(column=0, row=4, sticky='w')
frame.grid(column=0, row=0, sticky='w')

#drill frame
mypath = Path(candles.base_cache_dir) / candles.figi
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

drill_frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 8])

# candle file combobox
def choseCandle(entry):
    fullname = Path(candles.base_cache_dir) / candles.figi / entry
    candles.create_candle_df(fullname)  

candlecombo = Pmw.ComboBox(drill_frame, label_text='candle file:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        selectioncommand=choseCandle,
                        scrolledlist_items=onlyfiles)

candlecombo.grid(column= 0, row=0, sticky = 'w', padx=8, pady=8)
candle_filename = os.path.basename(candles.candle_file) 
candlecombo.selectitem(candle_filename)
choseCandle(candle_filename)

trading_label = ttk.Label(drill_frame, text="Trading file name:")
trading_label.grid(column=1, row=0, sticky='w') 
trading_entry = ttk.Entry(drill_frame)
trading_entry.grid(column=2, row=0, sticky='w') 

# trading_label = ttk.Label(drill_frame, text="Time:")
# trading_label.grid(column=3, row=0, sticky='w') 
# trading_entry = ttk.Entry(drill_frame)
# trading_entry.grid(column=4, row=0, sticky='w') 
# candle file combobox

def choseTime(entry):
    print('time chosen: ' + str(entry)) 

timecombo = Pmw.ComboBox(drill_frame, label_text='Time:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        selectioncommand=choseTime,
                        scrolledlist_items=[str(t) for t in candles.df.index])

timecombo.grid(column= 3, row=0, sticky = 'w', padx=8, pady=8)
timecombo.selectitem(str(candles.df.index[0]))
choseTime(candles.df.index[0])

drill_frame.grid(column=0, row=1, sticky='w', padx=8, pady=8)

root.mainloop()