'''
Created on Apr 23, 2015

@author: Malk
'''
from PIL import ImageTk, Image
from tkinter import *
from tkinter.ttk import *

from casper.generator import config

class GenerateFrame():

    def __init__(self, parent):
        self.createStyles()
        
        self.parent = parent
        self.frame = ttk.Frame(parent.frame, padding = "3 3 12 12")
        self.frame.pack(fill = BOTH, expand = 1)
        
    def render(self, generator):
        self.currentGenerator = generator
        self.clearContent()
        self.createHeader()
        self.createCenter()
        self.createFooter()
    
    def clearContent(self):
        for child in self.frame.winfo_children():
            child.destroy()
            
    def createStyles(self):
        pass
    
    def createHeader(self):
        self.header = ttk.Frame(self.frame);
        self.header.pack(fill = X)
        
        ttk.Button(self.header, text = config.GUI['MAIN']['HOME'], command = self.onHome).grid(column = 0, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 1, row = 0)
        ttk.Button(self.header, text = self.currentGenerator.name, command = self.onEdit).grid(column = 2, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 3, row = 0)
        ttk.Label(self.header, text = config.GUI['GENERATORS']['GENERATE']).grid(column = 4, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame, padding = '0 0 0 3')
        self.center.pack(fill = BOTH, expand = 1)
        
        ttk.Separator(self.center, orient = HORIZONTAL).pack(fill = X)
        #ttk.Label(self.center, text = self.currentGenerator.name, font = "Helvetica 14", anchor = W).pack(fill = X)
        self.createRandomEntryPanel(self.center)  
        
    def createFooter(self):
        self.footer = ttk.Frame(self.frame)
        self.footer.pack(fill = X)
    
    def createRandomEntryPanel(self, parent):
        for block in self.currentGenerator.blocks:
            frame = ttk.Frame(parent, padding = '0 0 0 5')
            frame.pack(fill = X)
            ttk.Label(frame, text = block.blockName, font = "Helvetica 13", anchor = W).pack(fill = X)
            
            randomParagraph = block.readRandom()
            if randomParagraph is None:
                ttk.Label(frame, text = config.GUI['GENERATORS']['NO_DATA'], anchor = W).pack(fill = X)
                ttk.Separator(frame, orient = HORIZONTAL).pack(fill = X)
                continue
            
            descriptionFrame = ttk.Frame(frame)
            descriptionFrame.pack(fill = BOTH)
            
            imageFilename = randomParagraph[3]
            if imageFilename is not '':
                imageObj = Image.open(self.currentGenerator.getImagesPath() + imageFilename)
                img = ImageTk.PhotoImage(imageObj)
                ttk.Label(descriptionFrame, image = img).pack(side = LEFT)
            else:
                ttk.Label(descriptionFrame, text = config.GUI['GENERATORS']['NO_IMAGE']).pack(side = LEFT)
            
            ttk.Label(descriptionFrame, text = randomParagraph[1]).pack(side = LEFT)
            
            ttk.Separator(frame, orient = HORIZONTAL).pack(fill = X)
        
    def onHome(self):
        self.parent.renderChooseGeneratorsFrame()
        
    def onEdit(self):
        self.parent.renderEditGeneratorFrame(self.currentGenerator)