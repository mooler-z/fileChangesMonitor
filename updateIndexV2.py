import sys, sqlite3, datetime as dt
from os.path import getmtime, join, exists, dirname, basename, isdir
from os import walk, listdir
from time import ctime as strtime


conn = sqlite3.connect(sys.argv[1])
curs = conn.cursor()

def selectorOne(table_name, **kwargs):
    '''select one row only'''
    items_q = "SELECT * FROM {} where basename=\"{}\" and dirname=\"{}\"".format(table_name, kwargs['basename'], kwargs['dirname'])
    curs.execute(items_q)
    return curs.fetchone()

def selectorAllDirs(table_name, **kwargs):
    '''select all directories from the parent folder'''
    items_q = "SELECT * FROM {} where dirname=\"{}\" and file_dir=1".format(table_name, kwargs['dirname'])
    curs.execute(items_q)
    return curs.fetchall()

def selectorAllFiles(table_name, **kwargs):
    '''select all files from the parent folder'''
    items_q = "SELECT * FROM {} where dirname=\"{}\" and file_dir=0".format(table_name, kwargs['dirname'])
    curs.execute(items_q)
    return curs.fetchall()

def selectorAll(table_name, **kwargs):
    '''select all directories and files from the parent folder'''
    items_q = "SELECT * FROM {} where dirname=\"{}\"".format(table_name, kwargs['dirname'])
    curs.execute(items_q)
    return curs.fetchall()

def selectorAllDirsOnly(table_name):
    '''select all directories and files from the parent folder'''
    items_q = "SELECT * FROM {} where file_dir=1".format(table_name)
    curs.execute(items_q)
    return curs.fetchall()

def deleteOne(table_name, **kwargs):
    '''delete one row with that particular file name and
    parent folder'''
    del_q = "DELETE FROM {} where basename=\"{}\" and dirname=\"{}\"".format(table_name, kwargs['basename'], kwargs['dirname'])
    curs.execute(del_q)
    conn.commit()

def deleteAll(table_name, dirname):
    '''delete all rows with that particular file name and
    parent folder'''
    del_q = "DELETE FROM {} where dirname=\"{}\"".format(table_name, dirname)
    curs.execute(del_q)
    conn.commit()
    
def insertToTable(table_name, items):
    query = "INSERT INTO {} VALUES (?,?,?,?)".format(table_name)
    curs.execute(query, items)
    conn.commit()
    
def updateOne(table_name, mod_time, **kwargs):
    query = "UPDATE {} SET mod_time={} WHERE basename=\"{}\" and dirname=\"{}\"".format(table_name, mod_time, kwargs['basename'], kwargs['dirname'])
    curs.execute(query)
    conn.commit()
    
def updateAll(table_name, mod_time, dirname):
    query = "UPDATE {} SET mod_time={} WHERE dirname=\"{}\"".format(table_name, mod_time, dirname)
    curs.execute(query)
    conn.commit()
    
def executeManyIns(table_name, queries):
    query = "INSERT INTO {} VALUES (\"{}\",\"{}\",{},{});"
    if queries:
        q_s = "\n".join([query.format(table_name, i[0], i[1], i[2], i[3]) for i in queries])
        curs.executescript(q_s)
        conn.commit()
    
def executeManyDels(table_name, queries):
    query = "DELETE FROM {} WHERE basename=\"{}\" and dirname=\"{}\";"
    if queries:
        q_s = "\n".join([query.format(table_name, i[0], i[1]) for i in queries])
        curs.executescript(q_s)
        conn.commit()
    
def firstWalk(abspath):
    db_walk = []
    for i in listdir(abspath):
        item = join(abspath, i)
        db_walk.append((i, abspath, getmtime(item), int(isdir(item))))
    return db_walk

def arrDiffIns(dbList, osList):
    for i in osList:
        if i not in dbList:
            insertToTable(sys.argv[2], i)

def arrDiffDel(dbList, osList):
    for i in dbList:
        if i not in osList:
            deleteOne("pic", basename=i[0], dirname=i[1])

selected = selectorAllDirsOnly(sys.argv[2])
selected.sort(key=lambda x: x[2])
for _dir in selected[::-1]:
    abspath = join(_dir[1], _dir[0])
    if exists(abspath):
        if strtime(getmtime(abspath)) != strtime(_dir[2]):
            db_walk = selectorAll(sys.argv[2], dirname=abspath)
            os_walk = firstWalk(abspath)
            arrDiffIns(db_walk, os_walk)
            arrDiffDel(db_walk, os_walk)