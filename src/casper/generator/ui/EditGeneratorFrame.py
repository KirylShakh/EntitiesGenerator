'''
Created on Nov 19, 2014

@author: Malk
'''
from tkinter import ttk

from tkinter import *
from tkinter.ttk import *

from casper.generator import config

class EditGeneratorFrame():
    
    # parent - parent ui object, has .frame property that current object should render its frame into
    # frame - ttk object, main frame of this ui object
    # currentGenerator - Generator currently loaded into this panel
    # activeBlock - Block currently loaded into Edit panel
    # header - ttk frame containing breadcrumb and such
    # center - ttk frame (?) containing all edit ui widgets
    # footer - ttk frame containing common buttons - close, generate random, back (?)
    # paragraphsPanel - ttk frame containing information about paragraphs of activeBlock
    # expandedFrame - frame that is currently expanded and can be accessed to collapse it in case other one need to be expanded
    
    def __init__(self, parent):
        style = ttk.Style()
        style.configure('EditGenFrame.TFrame', foreground='black', background='green') #padding does not work with frames 
        
        self.parent = parent
        self.frame = ttk.Frame(parent.frame, style='EditGenFrame.TFrame')
        self.frame.pack(expand=1, fill=BOTH)
        
        self.expandedFrame = None
        
    def render(self, generator):
        self.clearContent()
        
        self.currentGenerator = generator 
        
        self.createHeader()
        self.createCenter()
        self.createFooter()        
    
    def clearContent(self):
        self.clearWidgetContent(self.frame)
            
    def clearWidgetContent(self, widget):
        for child in widget.winfo_children(): #TODO: tkinter error here in some cases; need to investigate 
            child.destroy()    
    
    def createHeader(self):
        style = ttk.Style()
        style.configure('EditGenHeader.TFrame', background='red')
        
        self.header = ttk.Frame(self.frame, padding='0 5 0 5', style='EditGenHeader.TFrame')
        self.header.grid(column = 0, row = 0, sticky=(E, W))
        
        ttk.Button(self.header, text=config.GUI['MAIN']['HOME'], command = self.onHome).grid(column = 0, row = 0)
        ttk.Label(self.header, text=self.currentGenerator.name).grid(column = 1, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame)
        self.center.grid(column = 0, row = 1, sticky=(N, S, E, W))
        
        blocksFrame = ttk.Frame(self.center)
        blocksFrame.grid(column = 0, row = 0, sticky=(N, S, W))
        
        self.createBlocksPanel(blocksFrame)
        self.createParagraphsPanel(self.center)
        
    def createFooter(self):
        self.footer = ttk.Frame(self.frame)
        self.footer.grid(column = 0, row = 2, sticky=(E, W))

    def createBlocksPanel(self, parent):
        row = 0
        addBlockNameEntry = StringVar()
        ttk.Entry(parent, width=10, textvariable=addBlockNameEntry).grid(column = 0, row = row)
        
        ttk.Button(parent, text=config.GUI['MAIN']['ADD'], command = lambda addBlockNameEntry = addBlockNameEntry: self.onAddBlock(addBlockNameEntry)).grid(column = 1, row = row)
        row = row + 1
         
        index = row
        for block in self.currentGenerator.blocks:
            ttk.Button(parent, text=block.blockName, command = lambda block = block : self.loadBlock(block)).grid(column = 0, row = index)
            ttk.Button(parent, text=config.GUI['MAIN']['REMOVE'], command = lambda blockId = block.blockId : self.onDeleteBlock(blockId)).grid(column = 1, row = index)
            index = index + 1
            
    def createParagraphsPanel(self, parent):
        self.paragraphsPanel = ttk.Frame(self.center)   
        self.paragraphsPanel.grid(column = 1, row = 0, sticky=(N, S, E))
        
    def loadBlock(self, block):
        self.paragraphsPanel.destroy()
        self.createParagraphsPanel(self.center)
        paragraphsPanel = self.paragraphsPanel
        
        self.activeBlock = block
        row = 0
        
        ttk.Label(paragraphsPanel, text=self.activeBlock.blockName).grid(column = 0, row = row)
        row = row + 1
        
        row = self.createAddParaPanel(paragraphsPanel, row)
        row = self.createParaListPanel(paragraphsPanel, row)
    
    def createAddParaPanel(self, parent, row):
        frame = ttk.Frame(parent)
        frame.grid(column = 0, row = row)
        
        self.createAddParaCollapsedPanel(frame)
        return row + 1
    
    def createAddParaCollapsedPanel(self, parent):
        ttk.Button(parent, text=config.GUI['MAIN']['ADD'], command = lambda frame = parent: self.onAddParaPanelExpand(frame)).grid(column = 0, row = 0, sticky=(W, E))
    
    def createAddParaEditPanel(self, parent):
        addParaWidget = Text(parent, width=40, height=10)
        addParaWidget.grid(column = 0, row = 0)
        ttk.Button(parent, text=config.GUI['MAIN']['ADD'], command = lambda textWidget = addParaWidget: self.onAddParagraph(textWidget)).grid(column = 1, row = 0)
        
        if self.expandedFrame is not None:
            self.clearWidgetContent(self.expandedFrame)
        self.expandedFrame = parent
        
    def onAddParaPanelExpand(self, parent):
        self.clearWidgetContent(parent)
        self.createAddParaEditPanel(parent)
        
    def onAddParaPanelCollapse(self, parent):
        self.clearWidgetContent(parent)
        self.createAddParaCollapsedPanel(parent)
    
    def createParaListPanel(self, parent, row):
        index = row
        for row in self.activeBlock.read():
            ttk.Label(parent, text=row[1]).grid(column = 0, row = index)
            ttk.Button(parent, text=config.GUI['MAIN']['REMOVE'], command = lambda rowId = row[0]: self.onDeleteParagraph(rowId)).grid(column = 1, row = index)
            index = index + 1
        return index
    
    
        
    def onAddBlock(self, blockNameValue):
        try:
            name = blockNameValue.get()
        except ValueError:
            pass
        
        self.currentGenerator.addBlock(name)
        
        self.center.destroy()
        self.createCenter()    
    
    def onDeleteBlock(self, blockId):
        self.currentGenerator.deleteBlock(blockId)
        
        self.center.destroy()
        self.createCenter()
        
    def onAddParagraph(self, textWidget):
        name = textWidget.get('1.0', 'end')
        
        self.activeBlock.addParagraph(name)
        self.loadBlock(self.activeBlock)
        
    def onDeleteParagraph(self, rowId):
        self.activeBlock.deleteParagraph(rowId)
        self.loadBlock(self.activeBlock)
    
    def onHome(self):
        self.parent.renderChooseGeneratorsFrame()