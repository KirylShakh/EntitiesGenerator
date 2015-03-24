import unittest

from casper.generator.data.dbUtil import createDB, Table, Record
from casper.generator import config

class dbUtilTest(unittest.TestCase):
    
    def setUp(self):
        path = 'e:\\Development\\Workspaces\\Aptana\\Generator\\res\\'
        #path = 'D:\\Generator\\Workspace\\Generator\\res\\'
        config.init(path)
        self.inst = createDB('example')
        
        configTable = Table(self.inst, 'config', ['key varchar(255) unique', 'value text'])
        configTable.create()
        configTable.insert(['generator', 'example'])

    def tearDown(self):
        self.inst.remove()

    def testTable(self):
        t = Table(self.inst, 'tornados', ['power varchar(255) unique', 'coolness text'])
        t.create()
        t.insert(['over 9000', 'unimaginable'])
        t.insert(['asteroid-fall', 'meh'])
        
        for row in self.inst.execute('select power, coolness from tornados'):
            if row[0] == 'over 9000':
                self.assertEqual(row[1], 'unimaginable')
            else:
                self.assertEqual(row[1], 'meh')
                
        config = Table(self.inst, 'config', ['key', 'value'])
        record = config.insert(['block', 'tornados'])
        self.assertEqual(2, record.key)
        self.assertEqual('2', record.id())
        
        
    def testRecord(self):
        r = Record(self.inst, 'config', 1)
        row = r.read()
        
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], 'generator')
        self.assertEqual(row[2], 'example')
        
        row = r.read(['key', 'value'])
        self.assertEqual(row[0], 'generator')
        self.assertEqual(row[1], 'example')
        
        row = r.read('value')
        self.assertEqual(row[0], 'example')
        row = r.read('*', ('key', 'generator')) 
        self.assertEqual(row[2], 'example')
        row = r.read('*', 'id') 
        self.assertEqual(row[2], 'example')
        row = r.read('value', [('id', '1'), ('key', 'generator')]) 
        self.assertEqual(row[0], 'example') 
        
        r = Record(self.inst, 'config')
        r.read('*', ('key', 'generator'))  
        self.assertEqual(r.key, 1)
        self.assertEqual(r.id(), '1')                     


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testTable']
    unittest.main()