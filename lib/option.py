from tkinter import Tk
from tkinter import simpledialog as Dialog

import yaml
import Pmw

class Option():
    def __init__(self, futures_names, 
                 start_date, end_date, interval,
                 name='./csv_files/futures_options.csv',
                 default_futureindex = 593):
        
        self.futures_names = futures_names
        self.window = None
        self.option_yaml = {'futures name': futures_names[default_futureindex],
                       'interval': interval.name,
                       'start_date': start_date,
                       'end_date': end_date, 
                       'file name': name}
    def show(self, master):
        self.window = master    
        
    # def body(self, master):
    #     self.tittle('Options' +  self.name)
    #     combobox = Pmw.ComboBox(master, label_text='Futures:', labelpos='wn',
    #                     listbox_width=0, dropdown=1,
    #                     # selectioncommand=choseEntry,
    #                     scrolledlist_items=self.futures_names)
    #     default_furture = self.option_yaml['furteres name']
    #     combobox.grid(column= 0, row=0, sticky = 'w', padx=8, pady=8)
    #     combobox.selectitem(default_furture)
        # Tk.Label(master, text=self.option_yaml['furtures name']).grid(row=0, sticky=W)
        
    def option_save(self):
        with open(self.option_yaml['file name'], 'w') as f:
            yaml.dump(self.option_yaml, f) 
        self.window.destroy()
            
    def option_load(self, file_name):
        with open(file_name, 'r') as f:
            self.option_yaml = yaml.safe_load(f)               

