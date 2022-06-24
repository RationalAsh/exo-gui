import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame, Button, Style
from tkinter.messagebox import showinfo
from tkinter import RIGHT, BOTH, RAISED, font

class Application(tk.Tk):
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

        # Decide what to do.
        if e.keysym == 'Down':
            self.listbox.select_clear(self.selected_set)
            self.selected_set = min(self.selected_set + 1, 1)
            self.listbox.select_set(self.selected_set)
        elif e.keysym == 'Up':
            self.listbox.select_clear(self.selected_set)
            self.selected_set = max(self.selected_set - 1, 0)
            self.listbox.select_set(self.selected_set)
        elif e.keysym == 'Enter':
            pass


    def button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')

if __name__ == '__main__':
    app = Application()
    app.mainloop()