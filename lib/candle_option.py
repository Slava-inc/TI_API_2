from tkinter import Tk
from datetime import datetime, timezone

import yaml
import Pmw
import tinkoff.invest as ti
from tkinter import *


class Option():
    def __init__(self, master, futures_names,
                 start_date, end_date, interval,
                 name='./csv_files/futures_options.csv',
                 default_futureindex = 593):
        
        self.window = master
        default_feature = futures_names[default_futureindex]
        self.futures_names = futures_names
        self.option_yaml = {'futures name': default_feature,
                       'interval': interval.name,
                       'start_date': start_date,
                       'end_date': end_date, 
                       'file name': name}

        # file_name, furtures, start_date, end_date, interval
        self.e_filename = Pmw.EntryField(master, labelpos=W,label_text = 'Option file name:',
            value = name)
        self.e_filename.grid(column=0, row=0, sticky='w') 
        self.combo_futrues = Pmw.ComboBox(master, label_text='Futures:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        # selectioncommand=choseEntry,
                        scrolledlist_items=futures_names)
        self.combo_futrues.grid(column= 0, row=1, sticky = 'w', padx=8, pady=8)
        self.combo_futrues.selectitem(default_feature)    
        
        self.e_startdate = Pmw.EntryField(master, labelpos=W,label_text = 'start date:',
            value = start_date.date().strftime("%Y/%m/%d"),
            validate = {'validator' : 'date', 'minstrict' : 0, 'maxstrict' : 0, 'fmt' : 'ymd'})
        self.e_startdate.grid(column=0, row=2, sticky='w')   
        self.e_enddate = Pmw.EntryField(master, labelpos=W,label_text = 'end date:',
            value = end_date.date().strftime("%Y/%m/%d"),
            validate = {'validator' : 'date', 'minstrict' : 0, 'maxstrict' : 0, 'fmt' : 'ymd'})
        self.e_enddate.grid(column=1, row=2, sticky='w') 
        
        interval_list =[ti.CandleInterval.CANDLE_INTERVAL_1_MIN.name,
                    ti.CandleInterval.CANDLE_INTERVAL_5_MIN.name,
                    ti.CandleInterval.CANDLE_INTERVAL_10_MIN.name,
                    ti.CandleInterval.CANDLE_INTERVAL_HOUR.name,
                    ti.CandleInterval.CANDLE_INTERVAL_4_HOUR.name,
                    ti.CandleInterval.CANDLE_INTERVAL_DAY.name,
                    ti.CandleInterval.CANDLE_INTERVAL_MONTH.name]
        
        self.combointerval = Pmw.ComboBox(master, label_text='Interval:', labelpos='wn',
                        listbox_width=0, dropdown=1,
                        # selectioncommand=choseEntry,
                        scrolledlist_items=interval_list)
        self.combointerval.grid(column= 0, row=4, sticky = 'w', padx=8, pady=8)
        self.combointerval.selectitem(ti.CandleInterval[interval.name].name)         

        # Button(master, text="Save",
        # command=self.option_save).grid(column= 0, row=5, sticky = 'w', padx=8, pady=8)
    
    def datetofile(self, in_date):
        out_date = datetime.strptime(in_date.replace('/', ''), '%Y%m%d')  
        return out_date.replace(tzinfo=timezone.utc)    
    
    def get_option(self):
        self.option_yaml = {'futures name':self.combo_futrues.get(),
                    'interval':self.combointerval.get(),
                    'start_date': self.datetofile(self.e_startdate.getvalue()),
                    'end_date': self.datetofile(self.e_enddate.getvalue()), 
                    'file name':  self.e_filename.getvalue()}    
    def option_save(self):
        
        with open(self.option_yaml['file name'], 'w') as f:
            yaml.dump(self.option_yaml, f) 
        # self.window.destroy()
            
    def option_load(self, file_name):
        with open(file_name, 'r') as f:
            self.option_yaml = yaml.load(f)            