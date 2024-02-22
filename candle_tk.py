import tkinter as tk
from tkinter import Tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import mplfinance as fplt
# import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timezone
import ast
import yaml
import sys
import os
import glob
sys.path.append(os.path.dirname(__file__)+ "/..")
if __package__:
    from .lib.candles import Candles
    from .lib.drills import Drills
else:
    from lib.candles import Candles
    from lib.drills import Drills
import tinkoff.invest as ti
import id.basek
import id.accid
import Pmw
from Get_Futures_Shares_List import Futures
from os import listdir
from os.path import isfile, join
from pathlib import Path
from lib.candle_option import Option

global start_date, end_date, default_feature, tf

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

try:
    with open('./csv_files/futures_options.csv', 'r') as f:
        option_yaml = yaml.safe_load(f) 
        
    tf = ti.CandleInterval[option_yaml['interval']]
    start_date = option_yaml['start_date']
    end_date = option_yaml['end_date']
    default_feature = option_yaml['futures name']
except:
    option_yaml = None

CandleOption = None

root = Tk()

def on_close(window):
    global option_yaml, start_date, end_date, default_feature, tf, candles
    
    if messagebox.askokcancel("Save", "Do you want to save?"):
        CandleOption.get_option()
        option_yaml = CandleOption.option_yaml
        tf = ti.CandleInterval[option_yaml['interval']]
        start_date = option_yaml['start_date']
        end_date = option_yaml['end_date']
        default_feature = option_yaml['futures name'] 
        candles.create(start_date=start_date, end_date=end_date, interval=tf, figi=chosen_future.future_figi, futures=True)
        
        # option_yaml['start_date'] = candles.start_date.replace(hour=candles.start_hour, minute=0, second=0)
        # option_yaml['end_date'] = candles.end_date.replace(hour=candles.end_hour, minute=0, second=0)
        # CandleOption.option_yaml = option_yaml
        # CandleOption.option_save()   
        path = candles.get_candle_path(basename=False).replace('./', '')
        candlecombo.selectitem(path)
        
    window.destroy()
    candles.get_drawing(chosen_future.future_figi)
    canvas.draw()
    # candles_load()
    
    
def candle_options():
    global CandleOption
    
    w_option = Tk()
    w_option.title("candle options")
    w_option.geometry("450x120")

    # w_option.protocol("WM_DELETE_WINDOW", on_close)
    w_option.protocol("WM_DELETE_WINDOW", lambda: on_close(w_option))
    CandleOption = Option(w_option, futures_names, start_date=start_date, end_date=end_date, interval=tf)
    

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

    
    
menu_bar = Menu(frame)  # menu begins
file_menu = Menu(menu_bar, tearoff=0)
# all file menu-items will be added here next
menu_bar.add_cascade(label='File', menu=file_menu)
edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

def candles_load():
    # TODO debug
    candles.create(start_date=start_date, end_date=end_date, interval=tf, figi=chosen_future.future_figi, futures=True)
    candles.get_all_candles_from_cache()
    candles.get_drawing(chosen_future.future_figi)
    canvas.draw()

def drill_start():
    pass

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='candles', command=candles_load)
run_menu.add_command(label='drills', command=drill_start)
menu_bar.add_cascade(label='Run', menu=run_menu)

option_menu = Menu(menu_bar, tearoff=0)
option_menu.add_command(label='candles', command=candle_options)
menu_bar.add_cascade(label='Options',  menu=option_menu)

about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About',  menu=about_menu)
root.config(menu=menu_bar)  # menu ends

# if ~(option_yaml == None):
# TODO for all kind in portfolio
candles.create(start_date=start_date, end_date=end_date, interval=tf, figi=chosen_future.future_figi, futures=True)
candles.get_all_candles_from_cache()
start_date = candles.start_date
end_date = candles.end_date
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
onlyfiles = [os.path.basename(x) for x in glob.glob(str(mypath) + '\*.csv')]

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
# drills = Drills(chosen_future, )
root.mainloop()