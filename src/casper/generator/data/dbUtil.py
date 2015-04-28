'''
Created on Nov 19, 2014

@author: Malk
'''

import sqlite3
import os
import codecs
import shutil

from casper.generator import config

class Instance():
    dbName = ''
    conn = None
    cursor = None
    
    def __init__(self, dbName):
        self.dbName = dbName
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()
        
    def commit(self):
        self.conn.commit()
            
    def close(self):
        self.conn.close()
            
    def execute(self, command, params = None):
        if params is None:
            return self.cursor.execute(command)
        else:
            return self.cursor.execute(command, params)
        
    def remove(self):
        self.close()
        shutil.rmtree(self.dbName[:self.dbName.rfind('\\') + 1])
        
    def lastInsertedRowId(self):
        return self.cursor.lastrowid

def openDB(dbName):
    return Instance(config.DATA_PATH + dbName + '.gen' + '\\' + dbName + '.db')
    
def createDB(dbName):
    dbDir = config.DATA_PATH + dbName + '.gen'
    os.makedirs(dbDir)
    imgDir = dbDir + '\\' + 'images'
    os.makedirs(imgDir)
    return Instance(dbDir + '\\' + dbName + '.db')
    
class Table():

    instance = None    
    name = ''
    fields = []

    """
    name - table name as in database schema
    fields - array of sql description of fields from which table consists without primary key field which is added automatically as integer 'id' (e.g. ['key varchar(255) unique', 'value text']) 
    """    
    def __init__(self, instance, name, fields):
        self.instance = instance
        self.name = name
        self.fields = fields
        
    def create(self):
        self.instance.execute('create table {0}(id integer primary key asc, {1})'.format(quote(self.name), ', '.join(self.fields)))
        self.instance.commit()
        
    def read(self):
        return self.instance.execute('select * from {0}'.format(quote(self.name)))
    
    """
    fieldValues - array of values for new record in the order as fields were passed to table constructor
    """    
    def insert(self, fieldValues):
        fieldNames = [field[:field.find(' ')] if field.find(' ') != -1 else field for field in self.fields]
        fields = list(zip(*[fieldNames, fieldValues]))
        
        record = Record(self.instance, self.name)
        record.insert(fields)
        return record
    
    def update(self, rowId, fields):
        record = Record(self.instance, self.name, rowId)
        record.update(fields)
    
    def delete(self):
        self.instance.execute('drop table {0}'.format(quote(self.name)))
        self.instance.commit()
    
    def deleteRow(self, rowId):
        record = Record(self.instance, self.name, rowId)
        record.delete()
    
    def readRandom(self):
        for row in self.instance.execute('select * from {0} order by random() limit 1'.format(quote(self.name))):
            return row

class Record():
    
    instance = None
    table = ''
    key = None
    
    def __init__(self, instance, table = '', key = None):
        self.instance = instance
        self.table = table
        self.key = key
        
    def insert(self, fields):
        quotedFields = self.quoteFields(fields)
        keys = ', '.join([key for (key, _) in quotedFields])
        values = ', '.join([value for (_, value) in quotedFields])
        
        self.instance.execute('insert into {0} ({1}) values({2})'.format(quote(self.table), keys, values))
        self.instance.commit()
        self.key = self.instance.lastInsertedRowId() 
        
    def update(self, fields):
        quotedFields = self.quoteFields(fields)
        fieldsSet = ', '.join([key + '=' + value for (key, value) in quotedFields])
        
        self.instance.execute('update {0} set {1} where id={2}'.format(quote(self.table), fieldsSet, quote(self.id())))
        self.instance.commit()
        
    def delete(self):
        self.instance.execute('delete from {0} where id={1}'.format(quote(self.table), quote(self.id())))
        self.instance.commit()
        
    def read(self, fields = '*', by = 'id'):
        result = None
        for row in self.instance.execute('select {0} from {1} where {2}'.format(self.formatSelectFieldsCondition(fields), quote(self.table), self.formatByCondition(by))):
            result = row
        
        if self.key == None:
            self.readId(by)
        
        return result
    
    def readId(self, by):
        for row in self.instance.execute('select id from {0} where {1}'.format(quote(self.table), self.formatByCondition(by))):
            self.key = row[0]
    
    def formatSelectFieldsCondition(self, fields):
        if not isinstance(fields, str):
            return ', '.join([quote(field) for field in fields])
        elif fields != '*':
            return quote(fields)
        return fields
    
    def formatByCondition(self, by):
        if by == 'id':
            by = [(by, self.id())]
        if isinstance(by, tuple):
            by = [by]
        quoted = self.quoteFields(by)
        return ' AND '.join([key + '=' + value for (key, value) in quoted])
    
        
    def quoteFields(self, fields):
        if isinstance(fields, tuple):
            fields = [fields]
        return [(quote(key), quote(value)) for (key, value) in fields]
    
    def id(self):
        return str(self.key)


def quote(s, errors="strict"):
    encodable = s.encode("utf-8", errors).decode("utf-8")

    nul_index = encodable.find("\x00")

    if nul_index >= 0:
        error = UnicodeEncodeError("NUL-terminated utf-8", encodable,
                                   nul_index, nul_index + 1, "NUL not allowed")
        error_handler = codecs.lookup_error(errors)
        replacement, _ = error_handler(error)
        encodable = encodable.replace("\x00", replacement)

    return "\"" + encodable.replace("\"", "\"\"") + "\""


"""
                'create table config(id integer primary key asc, key varchar(255) unique, value text)',
                'create table periods(id integer primary key asc, title varchar(255) unique, description text, author integer, foreign key(author) references authors(id))',
                'create table events(id integer primary key asc, title varchar(255) unique, description text, author integer, period integer, foreign key(author) references authors(id), foreign key(period) references periods(id))',
                'create table scenes(id integer primary key asc, title varchar(255) unique, description text, author integer, question varchar(255), event integer, foreign key(author) references authors(id), foreign key(event) references events(id))',
                'create table focuses(id integer primary key asc, title varchar(255) unique, description text)',
                'create table focusesperiods(focus integer, period integer, foreign key(focus) references focuses(id), foreign key(period) references periods(id))',
                'create table focusesevents(focus integer, event integer, foreign key(focus) references focuses(id), foreign key(event) references events(id))',
                'create table focusesscenes(focus integer, scene integer, foreign key(focus) references focuses(id), foreign key(scene) references scenes(id))',
                'create table legacies(id integer primary key asc, title varchar(255) unique, description text, author ingteger, foreign key(author) references authors(id))',
                'create table legaciesperiods(legacy integer, period integer, foreign key(legacy) references legacies(id), foreign key(period) references periods(id))',
                'create table legaciesevents(legacy integer, event integer, foreign key(legacy) references legacies(id), foreign key(event) references events(id))',
                'create table legaciesscenes(legacy integer, scene integer, foreign key(legacy) references legacies(id), foreign key(scene) references scenes(id))',
                'create table authors(id integer primary key asc, name text unique)'
"""
