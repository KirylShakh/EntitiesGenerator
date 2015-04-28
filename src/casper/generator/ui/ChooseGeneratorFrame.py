'''
Created on Nov 19, 2014

@author: Malk
'''
import os

from tkinter import ttk, messagebox

from tkinter import *
from tkinter.ttk import *

from casper.generator import config
from casper.generator.ui import uiUtil

class ChooseGeneratorFrame():

    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent.frame, padding = "3 3 12 12")
        self.frame.pack(fill = BOTH, expand = 1)
        
    def render(self):
        self.clearContent()
        self.createHeader()
        self.createCenter()
        self.createFooter()
    
    def clearContent(self):
        uiUtil.clearWidgetContent(self.frame)

    def createHeader(self):
        self.header = ttk.Frame(self.frame, padding = '0 0 0 5');
        self.header.pack(fill = X)
        
        ttk.Label(self.header, text = config.GUI['MAIN']['HOME']).grid(column = 0, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame, padding = '0 0 0 3')
        self.center.pack(fill = BOTH, expand = 1)
        
        ttk.Separator(self.center, orient = HORIZONTAL).pack(fill = X)
        ttk.Label(self.center, text = config.GUI['GENERATORS']['TITLE'], font = "Helvetica 14", anchor = W).pack(fill = X)
        self.createNewGeneratorPanel(self.center)
        
        width = int(config.GUI['GENERATORS']['WIDTH'])
        height = int(config.GUI['GENERATORS']['HEIGHT'])
        genListFrame = uiUtil.addYScrollToFrame(self.center, width, height)
        self.createGeneratorListPanel(genListFrame)  
        
    def createFooter(self):
        self.footer = ttk.Frame(self.frame)
        self.footer.pack(fill = X)
    
    def createNewGeneratorPanel(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill = X)
        
        addGeneratorNameEntry = StringVar()
        ttk.Entry(frame, textvariable = addGeneratorNameEntry).pack(side = LEFT, fill = X, expand = 1)
        ttk.Button(frame, text = config.GUI['MAIN']['ADD'], style = 'AddRemoveGenerator.TButton', command = lambda addGeneratorNameEntry = addGeneratorNameEntry: self.createGenerator(addGeneratorNameEntry)).pack(side = LEFT)
        
    def createGenerator(self, generatorNameValue):
        try:
            name = generatorNameValue.get()
        except ValueError:
            pass
        
        self.parent.createGenerator(name)
        
    def createGeneratorListPanel(self, parent):
        names = []
        for (_, dirnames, _) in os.walk(config.DATA_PATH):
            names.extend(dirnames)
            break
        
        extension = ".gen"
        names = [name for name in names if name.endswith(extension)]
        names = [name[:-len(extension)] for name in names]
        
        listFrame = ttk.Frame(parent)
        listFrame.pack(fill = BOTH)
        for name in names:
            frame = ttk.Frame(listFrame)
            frame.pack(fill = X)
            ttk.Button(frame, text = name, width = int(config.GUI['GENERATORS']['NAME_WIDTH']), command = lambda generator = name : self.loadGenerator(generator)).pack(fill = X, side = LEFT, expand = 1)
            ttk.Button(frame, text = config.GUI['MAIN']['REMOVE'], style = 'AddRemoveGenerator.TButton', command = lambda generator = name : self.onDeleteGenerator(generator)).pack(side = LEFT)
            ttk.Button(frame, text = config.GUI['GENERATORS']['GENERATE'], command = lambda generator = name : self.onGenerate(generator)).pack(side = LEFT)
            
    def loadGenerator(self, name):
        self.parent.readGenerator(name)
    
    def onDeleteGenerator(self, name):
        result = messagebox.askquestion(config.GUI['MAIN']['DELETE'], config.GUI['MAIN']['SURE'])
        if result == 'yes':
            self.parent.deleteGenerator(name)
    
    def onGenerate(self, name):
        self.parent.generate(name)