import sqlite3
from sqlite3 import Error


def connect():
    try:
        conn = sqlite3.connect("./banco/tables.db")
        return conn
    except Error as e:
        print(e)

#class BD:

    #def insert(self):

    #def delete(self):

