from tkinter import *
import logging
from Game import Game

def donothing(event):
   filewin = Toplevel(root)
   button = Button(filewin, text="Do nothing button")
   button.pack()

def get_configuration():
    return "Default", "File"

if __name__ == "__main__":
    root = Tk()

    configuration, input = get_configuration()
    game = Game(configuration, input, root)

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff = 0)
    filemenu.add_command(label="Configure")
    filemenu.add_command(label="Run", command=game)
    filemenu.add_separator()
    filemenu.add_command(label = "Exit", command = root.quit)
    menubar.add_cascade(label = "File", menu = filemenu)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.config(menu = menubar)

    logging.basicConfig(level=logging.INFO)
    logging.debug('This will get logged')

    root.mainloop()
