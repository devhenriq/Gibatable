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

        conn.commit()
        conn.close()

    def delete(self, table, list):
        conn = self.connect(self)
        cur = conn.cursor()

        query = "DELETE FROM " + table + "WHERE "

        conn.commit()
        conn.close()

    def relatorio(self, table, cond = None):
        conn = self.connect(self)
        cur = conn.cursor()

        cond = " " + cond
        query = "SELECT * FROM " + table + cond

        cur.execute(query)
        print(cur.fetchall())
        return cur.fetchall()
        conn.commit()
        conn.close()


    def operation(self, query, list = None):
        conn = self.connect(self)
        cur = conn.cursor()

        cur.execute(query, list)

        conn.commit()
        conn.close()



