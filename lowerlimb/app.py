import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Lower Limb Exoskeleton')
        self.geometry('300x50')
        self.mainframe = ttk.Frame(self, padding="3 3 12 12")

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.pack()

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack()

        self.attributes("-fullscreen", True)

    def button_clicked(self):
        showinfo(title='Information',
                 message='Hello, Tkinter!')

if __name__ == '__main__':
    app = Application()
    app.mainloop()