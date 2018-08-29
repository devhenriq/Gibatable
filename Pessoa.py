import Banco
import sqlite3
class Pessoa:

    def __init__(self, cargo, quant, salario, categoria):
        self.cargo = cargo
        self.quant = quant
        self.salario = salario
        self.categoria = categoria
        self.provferias = None
        self.provdecimo = None
        self.fgts = None
        self.inss = None
        self.total = None
        self.calculoPessoal()

    def calculoPessoal(self):

        if self.categoria != "diretor":
            self.provferias = (self.salario/12)*0.333333
            self.provdecimo = self.salario/12
            self.fgts = (self.salario + self.provferias + self.provdecimo) * 0.08
            self.inss = (self.salario + self.provferias + self.provdecimo) * 0.258
            self.total = (self.salario + self.provdecimo + self.provferias + self.fgts + self.inss) * self.quant #enquanto usarmos este meio de quantidade de pessoas na função usaremos esse quant aqui

        else:
            self.inss = self.salario * 0.15
            self.total = (self.salario + self.inss) * self.quant
        print('uhul')
        self.insereBanco()

    def insereBanco(self):

        print("insere")
        conn = Banco.connect()
        cur = conn.cursor()

        str = 'pessoa (cargo, quant, salario, ferias, decimo, fgts, inss, total, categoria)'
        # cur.execute("\
        # INSERT INTO " + str + "\
        # VALUES (?,?,?,?,?,?,?,?,?)\
        # ", (self.cargo, self.quant, self.salario, self.provferias, self.provdecimo, self.fgts, self.inss, self.total, self.categoria))

        cur.execute("""SELECT * FROM pessoa""")

        print(cur.fetchall())

        conn.commit()
        conn.close()
