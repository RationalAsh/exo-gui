import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame, Button, Style
from tkinter.messagebox import showinfo
from tkinter import RIGHT, BOTH, RAISED, font
import os
from pathlib import Path

APPMODE = ''
SAVEFILE = ''

class ModeSelector(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Exo Manager')
        self.geometry('320x240')

        # Frame
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bind('<KeyPress>', self.keydown)

        default_font = font.Font(size=24, family='Courier')

        # Label
        msglabel = tk.Label(self.frame, text='Select an Option:')

        # Listbox with options
        options = tk.StringVar(value=('1. Record Experiment',
                                      '2. Tune Parameters'))
        self.listbox = tk.Listbox(self.frame, listvariable=options, height=2, selectmode='single', font=default_font)
        self.listbox.activate(1)
        self.listbox.pack(padx=1, pady=1)
        self.selected_set = 0
        self.listbox.select_set(self.selected_set)

        #self.attributes("-fullscreen", True)

    def keydown(self, e):
        """
        Respond to a keypress event.
        :param e:
        :return:
        """
        print('{}'.format(e))

        global APPMODE

        # Decide what to do.
        if e.keysym == 'Down':
            self.listbox.select_clear(self.selected_set)
            self.selected_set = min(self.selected_set + 1, 1)
            self.listbox.select_set(self.selected_set)
        elif e.keysym == 'Up':
            self.listbox.select_clear(self.selected_set)
            self.selected_set = max(self.selected_set - 1, 0)
            self.listbox.select_set(self.selected_set)
        elif e.keysym == 'Return':
            if self.selected_set == 0:
                APPMODE = 'RECORD'
            else:
                APPMODE = 'TUNE'
            self.destroy()

class DataRecordConfigurator(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Exo Manager - RECORD')
        self.geometry('320x240')

        # Frame
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bind('<KeyPress>', self.keydown)

        # State variable
        self.sel = 0

        default_font = font.Font(size=12, family='Courier')

        # Variables
        patient_code = tk.IntVar(value=1)
        session_num = tk.IntVar(value=1)
        record_num = tk.IntVar(value=1)

        # Labels
        b1 = tk.Radiobutton(self.frame, text='Patient #', value='PC', font=default_font)
        b1.grid(row=0, column=0)
        b2 = tk.Radiobutton(self.frame, text='Session #', value='PS', font=default_font)
        b2.grid(row=1, column=0)
        b3 = tk.Radiobutton(self.frame, text='Record  #', value='PR', font=default_font)
        b3.grid(row=2, column=0)

        self.rbuttons = [b1, b2, b3]

        b1.select()

        # Entries
        e1 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=patient_code)
        e1.grid(row=0, column=2)
        e2 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=session_num)
        e2.grid(row=1, column=2)
        e3 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=record_num)
        e3.grid(row=2, column=2)

        self.spinboxes = [e1, e2, e3]
        self.spinboxvars = [patient_code, session_num, record_num]

    def keydown(self, e):
        """
        Respond to a keypress event.
        :param e:
        :return:
        """
        print('{}'.format(e))

        global SAVEFILE

        # Decide what to do.
        if e.keysym == 'Up':
            self.sel = max(0, self.sel - 1)
            self.rbuttons[self.sel].select()
        elif e.keysym == 'Down':
            self.sel = min(2, self.sel + 1)
            self.rbuttons[self.sel].select()
        elif e.keysym == 'Right':
            cval = self.spinboxvars[self.sel].get()
            self.spinboxvars[self.sel].set(min(cval + 1, 4096))
        elif e.keysym == 'Left':
            cval = self.spinboxvars[self.sel].get()
            self.spinboxvars[self.sel].set(max(cval - 1, 0))
        elif e.keysym == 'Return':
            SAVEFILE = '/home/pi/Documents/EXPDATA/p{}/s{}/rec{}.csv'.format(self.spinboxvars[0].get(),
                                                                             self.spinboxvars[1].get(),
                                                                             self.spinboxvars[2].get())
            SAVEPATH = Path(SAVEFILE)

            # Make the parent path if it does not exist.
            #SAVEPATH.parent.mkdir()
            # Close the window
            self.destroy()

if __name__ == '__main__':
    modeSelectApp = ModeSelector()
    modeSelectApp.mainloop()

    if APPMODE == 'RECORD':
        recordApp = DataRecordConfigurator()
        recordApp.mainloop()

        print(SAVEFILE)