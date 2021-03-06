import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame, Button, Style
from tkinter.messagebox import showinfo
from tkinter import RIGHT, BOTH, RAISED, font
import os
from pathlib import Path
import serial
from serial.tools.list_ports import comports
import threading

RESOLUTION='480x480+0+0'

APPMODE = ''
SAVEFILE = ''

FULLSCREEN=False

def initialize_port():
    """
    Initialize the serial port.
    :return:
    """
    plist = comports()
    selected = []
    print("Checking for serial ports....")
    print("Found:")
    for i, p in enumerate(plist):
        print("{}. {}".format(i, p))
        if 'usbserial' in p.device:
            selected.append(p)
    print(selected)
    if len(selected) == 1:
        print("Selecting {}".format(selected[0]))
        return serial.Serial(selected[0].device, 500000)
    else:
        print("Could not find appropriate port.")
        return None

class ModeSelector(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Exo Manager')
        self.geometry(RESOLUTION)

        # Frame
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bind('<KeyPress>', self.keydown)

        if FULLSCREEN:
            self.attributes('-fullscreen', True)

        default_font = font.Font(size=20, family='Courier')
        large_font = font.Font(size=28, family='Courier')

        # Label
        msglabel = tk.Label(self.frame, text='Select an Option:', font=large_font)
        msglabel.pack(padx=5, pady=5)

        # Listbox with options
        options = tk.StringVar(value=('1. Record Session',
                                      '2. Tune Parameters'))
        self.listbox = tk.Listbox(self.frame, listvariable=options, height=2,
                                  selectmode='single', font=large_font)
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
        self.geometry(RESOLUTION)

        # Frame
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bind('<KeyPress>', self.keydown)

        # State variable
        self.sel = 0

        default_font = font.Font(size=20, family='Courier')
        large_font = font.Font(size=28, family='Courier')

        # Variables
        patient_code = tk.IntVar(value=1)
        session_num = tk.IntVar(value=1)
        record_num = tk.IntVar(value=1)

        # Labels
        heading_label_var = tk.StringVar()
        heading_label_var.set("Recording Details")
        heading_label = tk.Label(self.frame, textvariable=heading_label_var, relief=RAISED,
                                 font=large_font, pady=5, padx=5)
        heading_label.grid(row=0, columnspan=3)

        self.savefile_label_var = tk.StringVar()
        savefile_label = tk.Label(self.frame, textvariable=self.savefile_label_var, font=default_font,
                                  wraplength=320)
        savefile_label.grid(row=4, columnspan=3)

        b1 = tk.Radiobutton(self.frame, text='Patient #', value='PC', font=default_font,
                            pady=5, padx=5)
        b1.grid(row=1, column=0)
        b2 = tk.Radiobutton(self.frame, text='Session #', value='PS', font=default_font,
                            pady=5, padx=5)
        b2.grid(row=2, column=0)
        b3 = tk.Radiobutton(self.frame, text='Record  #', value='PR', font=default_font,
                            pady=5, padx=5)
        b3.grid(row=3, column=0)

        self.rbuttons = [b1, b2, b3]

        b1.select()

        # Entries
        e1 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=patient_code,
                        width=15, font=default_font)
        e1.grid(row=1, column=2)
        e2 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=session_num,
                        width=15, font=default_font)
        e2.grid(row=2, column=2)
        e3 = tk.Spinbox(self.frame, from_=1, to=4096, textvariable=record_num,
                        width=15, font=default_font)
        e3.grid(row=3, column=2)

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

        SAVEFILE = '/home/pi/Documents/EXPDATA/p{}/s{}/rec{}.csv'.format(self.spinboxvars[0].get(),
                                                                         self.spinboxvars[1].get(),
                                                                         self.spinboxvars[2].get())
        self.savefile_label_var.set("Saving to: " + SAVEFILE)

class DataRecorderApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Exo Manager - RECORD')
        self.geometry(RESOLUTION)

        # Frame
        self.frame = Frame(self, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.bind('<KeyPress>', self.keydown)

        # State variable
        self.sel = 0

if __name__ == '__main__':

    modeSelectApp = ModeSelector()
    modeSelectApp.mainloop()

    if APPMODE == 'RECORD':
        recordApp = DataRecordConfigurator()
        recordApp.mainloop()

        print(SAVEFILE)

