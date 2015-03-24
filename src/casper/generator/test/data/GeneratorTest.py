import unittest

from casper.generator.data.Generator import Generator
from casper.generator import config

class GeneratorTest(unittest.TestCase):
    
    def setUp(self):
        path = 'e:\\Development\\Workspaces\\Aptana\\Generator\\res\\'
        #path = 'D:\\Generator\\Workspace\\Generator\\res\\'
        config.init(path)
        self.g = Generator('taverns')
        self.g.create()

    def tearDown(self):
        self.g.remove()

    def testGenerator(self):
        self.g.read()
        self.assertEqual('taverns', self.g.name)
        
        self.g.name = 'Tavern generator'
        self.g.save()
        
        self.g.name = ''
        
        self.g.read()
        self.assertEqual('Tavern generator', self.g.name)
        
    def testGeneratorBlocks(self):
        self.g.read()
        
        self.g.blocksT.insert(['title', 'Title of the tavern'])
        self.g.blocksT.insert(['size', 'Size of the tavern: number of floors, etc'])
        
        self.g.readBlocks()
        titleBlock = self.g.blocks[0]
        self.assertEqual(1, titleBlock.blockId)
        self.assertEqual('title', titleBlock.blockName)
        self.assertEqual('Title of the tavern', titleBlock.description)
        
        titleBlock.create()
        titleBlock.insert(['U mamki', '<div>U mamki</div>', 'no image'])
        titleBlock.insert(['Tolstaya mamka', '<div><b>Tolstaya</b> mamka</div>', 'no image'])
        titleBlock.insert(['V shkole', '<div>Welcome to school</div>', 'no image'])
        
        sizeBlock = self.g.blocks[1]
        self.assertEqual(2, sizeBlock.blockId)
        self.assertEqual('size', sizeBlock.blockName)
        self.assertEqual('Size of the tavern: number of floors, etc', sizeBlock.description)
        
        sizeBlock.create()
        sizeBlock.insert(['Malovato mesta', '<div>malovato</div>', 'no image'])
        sizeBlock.insert(['Neobyatno', '<div><b>Over 9k</b></div>', 'no image'])
        
        titleRow1 = titleBlock.readRandom()
        sizeRow1 = sizeBlock.readRandom()
        print('1: {0} - {1} - {2} - {3}'.format(titleBlock.description, titleRow1[1], titleRow1[2], titleRow1[3]))
        print('1: {0} - {1} - {2} - {3}'.format(sizeBlock.description, sizeRow1[1], sizeRow1[2], sizeRow1[3]))
        
        titleRow2 = titleBlock.readRandom()
        sizeRow2 = sizeBlock.readRandom()
        print('2: {0} - {1} - {2} - {3}'.format(titleBlock.description, titleRow2[1], titleRow2[2], titleRow2[3]))
        print('2: {0} - {1} - {2} - {3}'.format(sizeBlock.description, sizeRow2[1], sizeRow2[2], sizeRow2[3]))
        
        self.assertTrue(titleRow1[1] != titleRow2[1] or sizeRow1[1] != sizeRow2[1], 'Chosen blocks are equal')
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTable']
    unittest.main()