'''
Created on Nov 19, 2014

@author: Malk
'''
import os
from shutil import copy

from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename

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
        self.createStyles()
        
        self.parent = parent
        self.frame = ttk.Frame(parent.frame, style = 'EditGenFrame.TFrame')
        self.frame.pack(fill = BOTH, expand = 1)
        
        self.collapser = None
        
    def render(self, generator):
        self.clearContent()
        
        self.currentGenerator = generator 
        
        self.createHeader()
        self.createCenter()
        self.createFooter()        
    
    def clearContent(self):
        self.clearWidgetContent(self.frame)
            
    def clearWidgetContent(self, widget):
        for child in widget.winfo_children(): 
            child.destroy()    
    
    def addYScrollToFrame(self, parentFrame, width, height):
        canvas = Canvas(parentFrame, highlightthickness = 0)
        scrollbar = Scrollbar(parentFrame, orient = 'vertical', command = canvas.yview)
        canvas.configure(yscrollcommand = scrollbar.set)
        
        scrollbar.pack(side = RIGHT, fill = Y)
        canvas.pack(side = LEFT, fill = BOTH, expand = 1)
        
        targetFrame = ttk.Frame(canvas)
        canvas.create_window((0,0), window = targetFrame, anchor = 'nw')        
        targetFrame.bind('<Configure>', lambda event, canvasCmp = canvas: canvasCmp.configure(scrollregion = canvasCmp.bbox('all'), width = width, height = height))
        
        return targetFrame
    
    def createStyles(self):
        style = ttk.Style()
        style.configure('EditGenFrame.TFrame')
        
        style = ttk.Style()
        style.configure('EditGenHeader.TFrame')
        
        style = ttk.Style()
        style.configure('EditGenCenter.TFrame', padding = '0 0 0 3' , background = 'gray')
        
        style = ttk.Style()
        style.configure('EditGenFooter.TFrame')
        
        style = ttk.Style()
        style.configure('AddRemoveBlock.TButton', width = 3)
        
        style = ttk.Style()
        style.configure('Block.TButton', width = 20, anchor = W)
        
        style = ttk.Style()
        style.configure('Para.TButton', width = 126, anchor = W)
        
        style = ttk.Style()
        style.configure('GlitchLabel.TLabel', width = 131, anchor = W)
    
    def createHeader(self):
        self.header = ttk.Frame(self.frame, padding = '0 5 0 5', style = 'EditGenHeader.TFrame')
        self.header.pack(fill=X)
        
        ttk.Button(self.header, text = config.GUI['MAIN']['HOME'], command = self.onHome).grid(column = 0, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 1, row = 0)
        ttk.Label(self.header, text = self.currentGenerator.name).grid(column = 2, row = 0)
        ttk.Label(self.header, text = config.GUI['MAIN']['SEP']).grid(column = 3, row = 0)
        ttk.Button(self.header, text = config.GUI['GENERATORS']['GENERATE'], command = self.onGenerate).grid(column = 4, row = 0)
        
    def createCenter(self):
        self.center = ttk.Frame(self.frame, style = 'EditGenCenter.TFrame')
        self.center.pack(fill = BOTH, expand = 1)

        ttk.Separator(self.center, orient = HORIZONTAL).pack(fill = X)        
        self.createSidePanel()
        ttk.Separator(self.center, orient = VERTICAL).pack(side = LEFT, fill = Y)
        self.createParagraphsPanel(self.center)
        
    def createFooter(self):
        self.footer = ttk.Frame(self.frame, style = 'EditGenFooter.TFrame')
        self.footer.pack(fill = X, side = BOTTOM)

    def createSidePanel(self):
        frameWidth = int(config.GUI['BLOCKS']['WIDTH'])
        frameHeight = int(config.GUI['BLOCKS']['HEIGHT'])
        
        sidePanel = ttk.Frame(self.center, width = frameWidth, padding = '0 0 3 0')
        sidePanel.pack(side = LEFT, fill = Y)
        
        ttk.Label(sidePanel, text = config.GUI['BLOCKS']['TITLE'], font = "Helvetica 14", anchor = W).pack(fill = X)
        self.createAddBlockPanel(sidePanel, frameWidth)
        ttk.Separator(sidePanel, orient = HORIZONTAL).pack(fill = X)
        
        blocksScrollingFrame = ttk.Frame(sidePanel, padding = '0 3 0 0')
        blocksScrollingFrame.pack()
        
        blocksFrame = self.addYScrollToFrame(blocksScrollingFrame, frameWidth, frameHeight)
        self.createBlocksPanel(blocksFrame)
        
    def createAddBlockPanel(self, sidePanel, width):
        addBlockFrame = ttk.Frame(sidePanel, width = width, padding = '0 0 0 3')
        addBlockFrame.pack()
        
        addBlockNameEntry = StringVar()
        ttk.Entry(addBlockFrame, width = 25, textvariable = addBlockNameEntry).pack(side = LEFT)
        ttk.Button(addBlockFrame, text = config.GUI['MAIN']['ADD'], style = 'AddRemoveBlock.TButton', command = lambda addBlockNameEntry = addBlockNameEntry: self.onAddBlock(addBlockNameEntry)).pack(side = LEFT)

    def createBlocksPanel(self, parent):
        row = 0
        index = row
        for block in self.currentGenerator.blocks:
            ttk.Button(parent, text = block.blockName, style = 'Block.TButton', command = lambda block = block : self.loadBlock(block)).grid(column = 0, row = index)
            ttk.Button(parent, text = config.GUI['MAIN']['REMOVE'], style = 'AddRemoveBlock.TButton', command = lambda blockId = block.blockId : self.onDeleteBlock(blockId)).grid(column = 1, row = index)
            index = index + 1
        
        if index == 0:
            ttk.Label(parent, text = config.GUI['BLOCKS']['EMPTY']).pack(fill = X)
        
    def createParagraphsPanel(self, parent):
        self.paragraphsPanel = ttk.Frame(parent, padding = '3 0 5 0')   
        self.paragraphsPanel.pack(side = LEFT, fill = BOTH, expand = 1)
        
    def loadBlock(self, block):
        self.collapser = None
        self.paragraphsPanel.destroy()
        self.createParagraphsPanel(self.center)
        paragraphsPanel = self.paragraphsPanel
        
        self.activeBlock = block
        
        ttk.Label(paragraphsPanel, text = self.activeBlock.blockName, font = "Helvetica 14", anchor = W).pack(fill = X)
        self.createAddParaPanel(paragraphsPanel)
        ttk.Separator(paragraphsPanel, orient = HORIZONTAL).pack(fill = X)
        
        paraScrollingFrame = ttk.Frame(paragraphsPanel, padding = '0 3 0 0')
        paraScrollingFrame.pack(fill = BOTH, expand = 1)
        
        paraListFrame = self.addYScrollToFrame(paraScrollingFrame, int(config.GUI['PARA']['WIDTH']), int(config.GUI['PARA']['HEIGHT']))
        self.createParaListPanel(paraListFrame)
    
    def createAddParaPanel(self, parent):
        frame = ttk.Frame(parent, padding = '0 0 0 3')
        frame.pack(fill = X)
        self.createAddParaCollapsedPanel(frame)
    
    def createAddParaCollapsedPanel(self, parent):
        ttk.Button(parent, text = config.GUI['PARA']['ADD'], command = lambda frame = parent: self.onAddParaPanelExpand(frame)).pack(fill = X)
    
    def createAddParaExpandedPanel(self, parent):
        ttk.Separator(parent, orient = HORIZONTAL).pack(fill = X)
        
        newLabelFrame = ttk.Frame(parent)
        newLabelFrame.pack(fill = X)
        ttk.Label(newLabelFrame, text = config.GUI['PARA']['NEW'], anchor = W).pack(side = LEFT, fill = X)
        ttk.Button(newLabelFrame, text = config.GUI['MAIN']['REMOVE'], style = 'AddRemoveBlock.TButton', command = lambda frame = parent: self.onAddParaPanelCollapse(frame)).pack(side = RIGHT)
        
        imageFilenameEntry = self.createBrowseImagePanel(parent)
        addParaWidget = Text(parent, height = int(config.GUI['PARA']['AREA_HEIGHT']))
        addParaWidget.pack(fill = X)
        ttk.Button(parent, text = config.GUI['MAIN']['ADD'], command = lambda textWidget = addParaWidget, imageWidget = imageFilenameEntry: self.onAddParagraph(textWidget, imageWidget)).pack(fill = X)
        
    def onAddParaPanelExpand(self, parent):
        if self.collapser is not None:
            self.collapser()
        self.collapser = lambda frame = parent: self.onAddParaPanelCollapse(frame)
        
        self.clearWidgetContent(parent)
        self.createAddParaExpandedPanel(parent)
        
    def onAddParaPanelCollapse(self, parent):
        self.collapser = None
        
        self.clearWidgetContent(parent)
        self.createAddParaCollapsedPanel(parent)
    
    def createParaListPanel(self, parent):
        exist = FALSE
        # some layout bug or my bad skills in this tkinter with canvases - when only 1 frame is rendered, its size is by whatever reason is reduced, 
        # so I render another widget in that case, and rendered frame becomes somehow dependant on that last widget size
        isOnePara = None 
        for row in self.activeBlock.read():
            exist = TRUE
            if isOnePara is None:
                isOnePara = TRUE
            elif isOnePara:
                isOnePara = FALSE
            
            paraFrame = ttk.Frame(parent, style = 'EditGenFooter.TFrame')
            paraFrame.pack(fill = X)
            self.createEditParaCollapsedPanel(paraFrame, row)
            
        if not exist:
            ttk.Label(parent, text = config.GUI['PARA']['EMPTY']).pack(fill = X)
        elif isOnePara:
            ttk.Label(parent, text = ' ', style = 'GlitchLabel.TLabel').pack(side = LEFT, fill = X)
    
    def createEditParaCollapsedPanel(self, parent, row):
        text = row[1]
        text = text.replace('\n', ' ')
            
        ttk.Button(parent, text = text, style = 'Para.TButton', command = lambda frame = parent, rowObj = row: self.onEditParaPanelExpand(frame, rowObj)).pack(side = LEFT, fill = X)
        ttk.Button(parent, text = config.GUI['MAIN']['REMOVE'], style = 'AddRemoveBlock.TButton', command = lambda rowId = row[0]: self.onDeleteParagraph(rowId)).pack(side = LEFT)
        
    def createEditParaExpandedPanel(self, parent, row):
        editLabelFrame = ttk.Frame(parent)
        editLabelFrame.pack(fill = X)
        ttk.Label(editLabelFrame, text = config.GUI['PARA']['EDIT'], anchor = W).pack(side = LEFT, fill = X)
        ttk.Button(editLabelFrame, text = config.GUI['MAIN']['REMOVE'], style = 'AddRemoveBlock.TButton', command = lambda frame = parent, rowObj = row: self.onEditParaPanelCollapse(frame, rowObj)).pack(side = RIGHT)
        
        imageFilenameEntry = self.createBrowseImagePanel(parent)
        imageFilename = row[3]
        if imageFilename is None:
            imageFilename = ''
        imageFilenameEntry.set(imageFilename)
        
        addParaWidget = Text(parent, height = int(config.GUI['PARA']['AREA_HEIGHT']))
        addParaWidget.insert('1.0', row[1])
        addParaWidget.pack(fill = X)
        ttk.Button(parent, text = config.GUI['MAIN']['EDIT'], command = lambda textWidget = addParaWidget, imageWidget = imageFilenameEntry, rowId = row[0]: self.onEditParagraph(textWidget, imageWidget, rowId)).pack(fill = X)

    def onEditParaPanelExpand(self, parent, row):
        if self.collapser is not None:
            self.collapser()
        self.collapser = lambda frame = parent: self.onEditParaPanelCollapse(frame, row)
        
        self.clearWidgetContent(parent)
        self.createEditParaExpandedPanel(parent, row)
        
    def onEditParaPanelCollapse(self, parent, row):
        self.collapser = None
        
        self.clearWidgetContent(parent)
        self.createEditParaCollapsedPanel(parent, row)
    
    def createBrowseImagePanel(self, parent):
        imageFrame = ttk.Frame(parent)
        imageFrame.pack(fill = X)
        
        imageFilenameEntry = StringVar()
        ttk.Button(imageFrame, text = config.GUI['PARA']['IMAGE'], command = lambda imageWidget = imageFilenameEntry: self.browseImageFilename(imageWidget)).pack(side = LEFT)
        ttk.Entry(imageFrame, textvariable = imageFilenameEntry).pack(side = LEFT, fill = X, expand = 1)
        
        return imageFilenameEntry
    
    def browseImageFilename(self, imageFilenameWidget):
        fname = askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"), ("All files", "*.*")))
        if fname is not None:
            imageFilenameWidget.set(fname)
        else:
            imageFilenameWidget.set('')

    def prepareImage(self, image):
        # image exists in current generator images folder
        if os.path.isfile(self.currentGenerator.getImagesPath() + image):
            return image
        
        # path is somehow broken, store empty path
        if not os.path.isfile(image):
            return ''
        
        newFilename = copy(image, self.currentGenerator.getImagesPath())
        return newFilename[newFilename.rfind('/') + 1:]
        
    def onAddBlock(self, blockNameValue):
        try:
            name = blockNameValue.get()
        except ValueError:
            pass
        
        self.currentGenerator.addBlock(name)
        
        self.center.destroy()
        self.createCenter()    
    
    def onDeleteBlock(self, blockId):
        result = messagebox.askquestion(config.GUI['MAIN']['DELETE'], config.GUI['MAIN']['SURE'])
        if result == 'no':
            return
        
        self.currentGenerator.deleteBlock(blockId)
        self.center.destroy()
        self.createCenter()
        
    def onAddParagraph(self, textWidget, imageWidget):
        name = textWidget.get('1.0', 'end')
        name = name.strip(' \t\n\r')
        
        try:
            image = imageWidget.get()
        except ValueError:
            pass
        image = self.prepareImage(image)
        
        self.activeBlock.addParagraph(name, image)
        self.loadBlock(self.activeBlock)
        
    def onEditParagraph(self, textWidget, imageWidget, rowId):
        result = messagebox.askquestion(config.GUI['MAIN']['EDIT'], config.GUI['MAIN']['SURE'])
        if result == 'no':
            return
        
        name = textWidget.get('1.0', 'end')
        name = name.strip(' \t\n\r')
        
        try:
            image = imageWidget.get()
        except ValueError:
            pass
        image = self.prepareImage(image)
        
        self.activeBlock.editParagraph(rowId, name, image)
        self.loadBlock(self.activeBlock)
        
    def onDeleteParagraph(self, rowId):
        result = messagebox.askquestion(config.GUI['MAIN']['DELETE'], config.GUI['MAIN']['SURE'])
        if result == 'no':
            return
        
        self.activeBlock.deleteParagraph(rowId)
        self.loadBlock(self.activeBlock)
    
    def onHome(self):
        self.parent.renderChooseGeneratorsFrame()
        
    def onGenerate(self):
        self.parent.renderGenerateFrame(self.currentGenerator)