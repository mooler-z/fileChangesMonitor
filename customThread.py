import os, time, sqlite3
from copy import deepcopy
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3

class SearchQueue(QThread):
    updateListSignal = pyqtSignal(list)
    
    def __init__(self, gen):
        super().__init__()
        print("Initializing")
        self.gen = gen
        os.system("python updateIndexV2.py docss.db pic &")
        print(gen)
        
    def one(self, que):
        conn = sqlite3.connect("docss.db")
        self.curs = conn.cursor()
        query = 'SELECT * FROM pic where basename like '
        queryList = que.split(" ")
        if len(queryList) == 1:
            query += '"%{}%"'.format(queryList[0])
            self.curs.execute(query)
        else:
            the_words = ""
            for i in queryList:
                the_words += f'%{i}%'
            query += '"{}"'.format(the_words)
            self.curs.execute(query)
        
    def run(self):
        self.one(self.gen)
        temp = self.curs.fetchall()
        temp.sort(key=lambda x: x[2])
        self.updateListSignal.emit(temp[::-1])
        
class LineEdit(QThread):
    updateLineEdit = pyqtSignal(str)
    
    def __init__(self, text):
        super().__init__()
        self.text = text
    
    def run(self):
        pass
