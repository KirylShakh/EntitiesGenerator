'''
Created on Nov 19, 2014

@author: Malk
'''
import os

import PIL.ImageTk
import PIL.Image
import time

from shutil import copy
from tkinter.filedialog import askopenfilename

from tkinter import *
from tkinter.ttk import *

from casper.generator import config

def clearWidgetContent(widget):
    for child in widget.winfo_children(): 
        child.destroy()    
    
def addYScrollToFrame(parentFrame, width, height):
    canvas = Canvas(parentFrame, highlightthickness = 0)
    scrollbar = Scrollbar(parentFrame, orient = 'vertical', command = canvas.yview)
    canvas.configure(yscrollcommand = scrollbar.set)
    
    scrollbar.pack(side = RIGHT, fill = Y)
    canvas.pack(side = LEFT, fill = BOTH, expand = 1)
    
    targetFrame = ttk.Frame(canvas, width = width, height = height)
    canvas.create_window((0,0), window = targetFrame, anchor = 'nw')
    #canvas.bind_all("<MouseWheel>", lambda event, canvasCmp = canvas: onMW(event, canvasCmp)) #commented for now as incomplete feature        
    targetFrame.bind('<Configure>', lambda event, canvasCmp = canvas: canvasCmp.configure(scrollregion = canvasCmp.bbox('all'), width = width, height = height))
    
    return targetFrame

def onMW(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def createStyles():
    style = ttk.Style()
    style.configure('MainFrame.TFrame')
    
    style = ttk.Style()
    style.configure('AddRemoveGenerator.TButton', width = 3)
    
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

def browseImageFilename(imageFilenameWidget):
    fname = askopenfilename(filetypes=(("Image files", "*.jpg;*.jpeg;*.png;*.gif"), ("All files", "*.*")))
    if fname is not None:
        imageFilenameWidget.set(fname)
    else:
        imageFilenameWidget.set('')

def prepareImage(imagesPath, image):
    # image exists in images folder and image is just a filename
    if os.path.isfile(imagesPath + image):
        return image
    
    # was chosen image from the generator images folder
    image = image.replace('/', '\\')
    filepath = image[:image.rfind('\\') + 1]
    filename = image[image.rfind('\\') + 1:]
    print('filepath')
    print(filepath)
    print('imagepath')
    print(imagesPath)
    if filepath == imagesPath and os.path.isfile(imagesPath + filename):
        return filename
    
    # path is somehow broken, store empty path
    if not os.path.isfile(image):
        return ''
    
    extension = filename[filename.rfind('.') + 1:]
    newFilename = str(time.time())
    newFilename = copy(image, imagesPath + newFilename + '.' + extension)
    return newFilename[newFilename.rfind('\\') + 1:]

def renderImage(imagesPath, parent, filename):
    previewW = int(config.GUI['GENERATORS']['PREVIEW_WIDTH'])
    previewH = int(config.GUI['GENERATORS']['PREVIEW_HEIGHT'])
    size = previewW, previewH
    
    imageObj = PIL.Image.open(imagesPath + filename)
    imageObj.thumbnail(size, PIL.Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(imageObj)
    
    canvas = Canvas(parent, bd = 0, highlightthickness = 0, width = previewW, height = previewH)
    canvas.create_image(0, 0, image = img, anchor = NW, tags = "IMG")
    canvas.image = img
    canvas.pack(side = LEFT)
