'''
Created on 25.11.2014

@author: Shakh_K
'''

from casper.generator import config
from casper.generator.data.dbUtil import createDB, openDB, Record, Table
from casper.generator.data.Block import Block

class Generator():
    
    instance = None
    dbName = ''
    name = ''
    
    configL = None
    blocksL = None
    
    def __init__(self, dbName):
        self.dbName = dbName
        self.configL = config.DB['TABLE_CONFIG']
        self.blocksL = config.DB['TABLE_BLOCKS']
    
    def create(self):
        self.instance = createDB(self.dbName)
        
        configT = Table(self.instance, self.configL['NAME'], [self.configL['KEY'] + ' varchar(255) unique', self.configL['VALUE'] + ' text'])
        configT.create()
        configT.insert([self.configL['KEY_GENERATOR'], self.dbName])
        self.name = self.dbName
        
        self.blocksT = Table(self.instance, self.blocksL['NAME'], [self.blocksL['BLOCK'] + ' varchar(31) unique', self.blocksL['DESCRIPTION'] + ' text'])
        self.blocksT.create()
        
        self.blocks = []
    
    def addBlock(self, name, description = ''):
        addedBlockRecord = self.blocksT.insert([name, description])
        addedBlock = Block(self.instance, addedBlockRecord.read())
        addedBlock.create()
        self.blocks.append(addedBlock)
        
    def deleteBlock(self, blockId):
        block = self.getBlock(blockId)
        block.delete()
        self.blocks.remove(block)
        
        self.blocksT.deleteRow(blockId)
        
    def open(self):
        self.instance = openDB(self.dbName)
        self.read()
        
    def read(self):
        self.blocksT = Table(self.instance, self.blocksL['NAME'], [self.blocksL['BLOCK'], self.blocksL['DESCRIPTION']])
        self.nameRecord = Record(self.instance, self.configL['NAME'])
        
        self.readName()
        self.readBlocks()
    
    def readName(self):
        self.name = self.nameRecord.read(self.configL['VALUE'], (self.configL['KEY'], self.configL['KEY_GENERATOR']))[0]
    
    def readBlocks(self):
        self.blocks = []
        for row in self.blocksT.read():
            self.blocks.append(Block(self.instance, row))
    
    def save(self):
        self.nameRecord.update((self.configL['VALUE'], self.name))
        
    def close(self):
        self.instance.close()
    
    def remove(self):
        self.instance.remove()
        
    def getBlock(self, blockId):
        for block in self.blocks:
            if block.blockId == blockId:
                return block
        
        return None