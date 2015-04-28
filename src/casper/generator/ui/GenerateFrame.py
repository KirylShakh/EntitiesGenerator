'''
Created on Apr 23, 2015

@author: Malk
'''
from tkinter import *
from tkinter.scrolledtext import ScrolledText

from casper.generator import config
from casper.generator.ui import uiUtil

class GenerateFrame():

    def __init__(self, parent):
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
        uiUtil.clearWidgetContent(self.frame)

    def createHeader(self):
        self.header = ttk.Frame(self.frame, padding = '0 0 0 5');
        self.header.pack(fill = X)
        
        ttk.Button(self.header, text = config.GUI['MAIN']['HOME'], command = self.onHome).grid(column = 0, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 1, row = 0)
        ttk.Button(self.header, text = self.currentGenerator.name, command = self.onEdit).grid(column = 2, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 3, row = 0)
        ttk.Button(self.header, text = config.GUI['GENERATORS']['GENERATE'], command = self.onGenerate).grid(column = 4, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame, padding = '0 0 0 3')
        self.center.pack(fill = BOTH, expand = 1)
        
        ttk.Separator(self.center, orient = HORIZONTAL).pack(fill = X)
        #ttk.Label(self.center, text = self.currentGenerator.name, font = "Helvetica 14", anchor = W).pack(fill = X)
        width = int(config.GUI['GENERATORS']['WIDTH'])
        height = int(config.GUI['GENERATORS']['HEIGHT'])
        randomEntryFrame = uiUtil.addYScrollToFrame(self.center, width, height)
        self.createRandomEntryPanel(randomEntryFrame)  
        
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
            descriptionFrame.pack(fill = BOTH, expand = 1)
            
            imageFilename = randomParagraph[3]
            if imageFilename is not '':
                uiUtil.renderImage(self.currentGenerator.getImagesPath(), descriptionFrame, imageFilename)
            else:
                Label(descriptionFrame, text = config.GUI['GENERATORS']['NO_IMAGE'], width = int(config.GUI['GENERATORS']['PREVIEW_LABEL_WIDTH']), height = int(config.GUI['GENERATORS']['PREVIEW_LABEL_HEIGHT'])).pack(side = LEFT)
            
            ttk.Separator(descriptionFrame, orient = VERTICAL).pack(side = LEFT, fill = Y)
            
            descriptionLabel = ScrolledText(descriptionFrame, wrap='word', width = int(config.GUI['GENERATORS']['DESCRIPTION_WIDTH']), height = int(config.GUI['GENERATORS']['PREVIEW_LABEL_HEIGHT']))
            descriptionLabel.insert(1.0, randomParagraph[1])
            descriptionLabel.pack(side = LEFT)
            descriptionLabel.configure(bg = self.parent.parent.cget('bg'), relief = 'flat', state = 'disabled')
            ttk.Separator(frame, orient = HORIZONTAL).pack(fill = X)
    
    def onHome(self):
        self.parent.renderChooseGeneratorsFrame()
        
    def onEdit(self):
        self.parent.renderEditGeneratorFrame(self.currentGenerator)
        
    def onGenerate(self):
        self.parent.renderGenerateFrame(self.currentGenerator)