'''
Created on Nov 19, 2014

@author: Malk
'''
from tkinter import ttk

from tkinter import *
from tkinter.ttk import *

from casper.generator import config
from casper.generator.data.Generator import Generator

from casper.generator.ui.ChooseGeneratorFrame import ChooseGeneratorFrame
from casper.generator.ui.EditGeneratorFrame import EditGeneratorFrame 
from casper.generator.ui.GenerateFrame import GenerateFrame

class MainFrame():
    '''
    Main frame class
    '''

    def __init__(self, parent):
        style = ttk.Style()
        style.configure('MainFrame.TFrame')
        
        self.parent = parent
        self.frame = ttk.Frame(parent, padding = "3 3 12 12", style = 'MainFrame.TFrame')
        self.frame.pack(expand = 1, fill = BOTH)
        
        self.renderChooseGeneratorsFrame()
        
    def renderChooseGeneratorsFrame(self):
        self.clearContent()
        self.activeFrame = ChooseGeneratorFrame(self)
        self.activeFrame.render()
    
    def renderEditGeneratorFrame(self, generator):
        self.clearContent()
        self.activeFrame = EditGeneratorFrame(self)
        self.activeFrame.render(generator)
        
    def renderGenerateFrame(self, generator):
        self.clearContent()
        self.activeFrame = GenerateFrame(self)
        self.activeFrame.render(generator)

    def clearContent(self):
        for child in self.frame.winfo_children():
            child.destroy()

    def createGenerator(self, name):
        generator = Generator(name)
        generator.create()
        self.renderEditGeneratorFrame(generator)
        
    def readGenerator(self, name):
        generator = Generator(name)
        generator.open()
        self.renderEditGeneratorFrame(generator)
    
    def deleteGenerator(self, name):
        generator = Generator(name)
        generator.open()
        generator.remove()
        generator = None
        self.renderChooseGeneratorsFrame()
        
    def generate(self, name):
        generator = Generator(name)
        generator.open()
        self.renderGenerateFrame(generator)