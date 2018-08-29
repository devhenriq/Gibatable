import sqlite3
from sqlite3 import Error
table = []
table.append("""
CREATE TABLE IF NOT EXISTS pessoa (
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   cargo TEXT NOT NULL,
   quant INTEGER NOT NULL,
   salario FLOAT NOT NULL,
   ferias FLOAT NOT NULL,
   decimo FLOAT NOT NULL,
   fgts FLOAT NOT NULL,
   inss FLOAT NOT NULL,
   total FLOAT NOT NULL,
   categoria TEXT NOT NULL
);""")

table.append("""
CREATE TABLE IF NOT EXISTS investimentofixo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    quant INTEGER NOT NULL,
    valorunitario FLOAT NOT NULL,
    total FLOAT NOT NULL,
    categoria TEXT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS materiaprima (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto TEXT NOT NULL,
    descricao TEXT NOT NULL,
    unmedida TEXT NOT NULL,
    precounitario FLOAT NOT NULL,
    quant INTEGER NOT NULL,
    total FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS estimativa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    quant INTEGER NOT NULL,
    lucrounitario FLOAT NOT NULL,
    mes INTEGER NOT NULL,
    lucrototal FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS custosfixos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maodeobra FLOAT NOT NULL,
    prolabore FLOAT NOT NULL,
    limpeza FLOAT NOT NULL,
    contador FLOAT NOT NULL,
    material FLOAT NOT NULL,
    agua FLOAT NOT NULL,
    aluguel FLOAT NOT NULL,
    manutencao FLOAT NOT NULL,
    deprec FLOAT NOT NULL,
    outros FLOAT NOT NULL,
    total FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS tributos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tributo TEXT NOT NULL,
    aliquota FLOAT NOT NULL,
    indice FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS custovendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    porcentagem FLOAT NOT NULL,
    indice FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS investimentoinicial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legalizacao FLOAT NOT NULL,
    divulgacao FLOAT NOT NULL,
    outros FLOAT NOT NULL,
    caixa FLOAT NOT NULL,
    total FLOAT NOT NULL
);""")

table.append("""CREATE TABLE IF NOT EXISTS custofinanceiro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    custo FLOAT NOT NULL,
);""")

table.append("""CREATE TABLE IF NOT EXISTS precovenda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mes INTEGER NOT NULL,
    outros FLOAT NOT NULL,
    total FLOAT NOT NULL,
);""")


def create_table(cursor, table):
    try:
        cursor.execute(table)
    except Error:
        print(Error)

conn = sqlite3.connect('tables.db')

cursor = conn.cursor()

for tab in table:
    create_table(cursor, tab)

print("tabela criada com sucesso")

conn.close()