'''
Created on 25.11.2014

@author: Shakh_K
'''

from casper.generator import config
from casper.generator.data.dbUtil import Table

class Block(Table):
    
    def __init__(self, instance, row):
        self.blockL = config.DB['TABLE_BLOCK']
        self.blockId = row[0]
        self.blockName = row[1]
        self.description = row[2]
        super().__init__(instance, self.blockName + str(self.blockId), [self.blockL['DESCRIPTION'] + ' text', self.blockL['HTML'] + ' text', self.blockL['IMAGE'] + ' text'])
        
    def addParagraph(self, description, image = '', html = ''):
        return self.insert([description, html, image])
        
    def editParagraph(self, rowId, description, image = None, html = None):
        fields = [(self.blockL['DESCRIPTION'], description)]
        if html is not None:
            fields.append((self.blockL['HTML'], html))
        if image is not None:
            fields.append((self.blockL['IMAGE'], image))
        self.update(rowId, fields)
        
    def deleteParagraph(self, paragraphId):
        self.deleteRow(paragraphId)
    