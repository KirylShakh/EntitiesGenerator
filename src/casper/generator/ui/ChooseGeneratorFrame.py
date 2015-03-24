'''
Created on Nov 19, 2014

@author: Malk
'''
from os import walk

from tkinter import ttk

from tkinter import *
from tkinter.ttk import *

from casper.generator import config
from casper.generator.data.Generator import Generator

class ChooseGeneratorFrame():

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent.frame, padding="3 3 12 12")
        self.frame.pack()
        
    def render(self):
        self.clearContent()
        self.createHeader()
        self.createCenter()
        self.createFooter()
    
    def clearContent(self):
        for child in self.frame.winfo_children():
            child.destroy()                
        
    def createHeader(self):
        self.header = ttk.Frame(self.frame);
        self.header.grid(column = 0, row = 0, sticky=(E, W))
        
        ttk.Label(self.header, text=config.GUI['MAIN']['HOME']).grid(column = 0, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame)
        self.center.grid(column = 0, row = 1, sticky=(N, S, E, W))
        
        self.createNewGeneratorPanel(self.center)
        self.createGeneratorListPanel(self.center)  
        
    def createFooter(self):
        self.footer = ttk.Frame(self.frame)
        self.footer.grid(column = 0, row = 2, sticky=(E, W))
    
    def createNewGeneratorPanel(self, parent):
        addGeneratorNameEntry = StringVar()
        ttk.Entry(parent, width=10, textvariable=addGeneratorNameEntry).grid(column = 0, row = 1)
        
        ttk.Button(parent, text=config.GUI['MAIN']['ADD'], command = lambda addGeneratorNameEntry = addGeneratorNameEntry: self.createGenerator(addGeneratorNameEntry)).grid(column = 1, row = 1)
        
    def createGenerator(self, generatorNameValue):
        try:
            name = generatorNameValue.get()
        except ValueError:
            pass
        
        self.parent.createGenerator(name)
        
    def createGeneratorListPanel(self, parent):
        files = []
        for (_, _, filenames) in walk(config.DATA_PATH):
            files.extend(filenames)
            break
        
        extension = ".db"
        files = [filename for filename in files if filename.endswith(extension)]
        files = [filename[:-len(extension)] for filename in files]
        
        index = 2
        for filename in files:
            ttk.Button(parent, text=filename, command = lambda generator = filename : self.loadGenerator(generator)).grid(column = 0, row = index)
            ttk.Button(parent, text="-", command = lambda generator = filename : self.onDeleteGenerator(generator)).grid(column = 1, row = index)
            index = index + 1
            
    def loadGenerator(self, name):
        self.parent.readGenerator(name)
    
    def onDeleteGenerator(self, name):
        self.parent.deleteGenerator(name)