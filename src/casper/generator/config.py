'''
Created on Nov 19, 2014

@author: Malk
'''
import os
from configparser import ConfigParser

class Config():
    data = 'data'
    images = 'images'
    strings = 'strings'
    path = None
    
    def __init__(self, path):
        self.path = path
        self.initStrings()
        self.initData()

    def initStrings(self):
        self.gui = ConfigParser()
        self.gui.read(self.filePath(self.strings, 'gui.ini'))
        
    def initData(self):
        self.db = ConfigParser()
        self.db.read(self.filePath(self.strings, 'db.ini'))
    
    def dirPath(self, dirName):
        return os.path.abspath(self.path + dirName) + '\\'
    
    def filePath(self, dirName, file=''):
        return os.path.abspath(self.path + dirName + '\\' + file)

def init(path = None):
    global config
    global GUI
    global DB
    global DATA_PATH
    
    if not path:
        path = os.getcwd() + '\\..\\..\\..\\res\\'
    
    config = Config(path)
    GUI = config.gui
    DB = config.db
    DATA_PATH = config.dirPath(config.data)
    
config = None
GUI = None
DB = None
DATA_PATH = None