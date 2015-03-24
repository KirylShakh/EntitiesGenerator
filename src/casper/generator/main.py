'''
Created on Nov 19, 2014

@author: Malk
'''

from tkinter import Tk

from casper.generator.ui.MainFrame import MainFrame
from casper.generator import config

def main():
    config.init()
    
    root = Tk()
    root.title(config.GUI['MAIN']['TITLE'])
    root.minsize(width=int(config.GUI['MAIN']['WIDTH']), height=int(config.GUI['MAIN']['HEIGHT']))
    
    mainFrame = MainFrame(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    