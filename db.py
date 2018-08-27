import sqlite3
from sqlite3 import Error

def connectDatabase(fileName):
    db = sqlite3.connect(fileName)
    return db

def closeDatabase(db):
    db.close()

def execute(db, query):
    cursor = db.cursor()
    ret = cursor.execute(query)
    db.commit()
    return ret
