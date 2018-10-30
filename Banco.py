import sqlite3
from sqlite3 import Error

class Banco:

    def __init__(self):
        print('empty')

    def connect(self):
        try:
            conn = sqlite3.connect("./banco/tables.db")
            return conn
        except Error as e:
            print(e)

    def insert(self, table, list):
        conn = self.connect(self)
        cur = conn.cursor()

        query = "INSERT INTO " + table + " VALUES ("

        for i in range(0, len(list)):
            if i != len(list)-1:
                query = query + "?,"
            else:
                query = query + "?)"
        cur.execute(query, (list))
        #print(query)
        #print(list)
        conn.commit()
        conn.close()

    def delete(self, table, col=None, cond = None):
        conn = self.connect(self)
        cur = conn.cursor()

        if col is None:
            col = ""
        if cond is None:
            cond = ""
        query = "DELETE " + col + " FROM " + table + cond
        #print(query)
        cur.execute(query)

        conn.commit()
        conn.close()

    def relatorio(self, table, col = None, cond = None):
        conn = self.connect(self)
        cur = conn.cursor()

        if col is None:
            col = "*"
        if cond is None:
            cond = ""
        query = "SELECT " + col + " FROM " + table + cond
        #print(query)
        cur.execute(query)
        ret = cur.fetchall()
        conn.commit()
        conn.close()
        return ret

    def update(self, table, col = None, cond = None):
        conn = self.connect(self)
        cur = conn.cursor()

        if col is None:
            col = "*"
        if cond is None:
            cond = ""
        query = "UPDATE " + table + " SET " + col + cond
        #print(query)
        cur.execute(query)
        ret = cur.fetchall()
        conn.commit()
        conn.close()
        return ret

    def operation(self, query, list = None):
        conn = self.connect(self)
        cur = conn.cursor()

        cur.execute(query, list)

        conn.commit()
        conn.close()



