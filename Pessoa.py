import Banco

class Pessoa:

    def __init__(self, cargo, quant, salario, categoria):
        self.cargo = cargo
        self.quant = quant
        self.salario = salario
        self.categoria = categoria
        self.provFerias = None
        self.provdecimo = None
        self.fgts = None
        self.inss = None
        self.total = None
        self.calculoPessoal()

    def calculoPessoal(self):

        if self.categoria != "diretor":
            self.provFerias = (self.salario/12)*0.333333
            self.provdecimo = self.salario/12
            self.fgts = (self.salario + self.provFerias + self.provdecimo) * 0.08
            self.inss = (self.salario + self.provFerias + self.provdecimo) * 0.258
            self.total = (self.salario + self.provdecimo + self.provFerias + self.fgts + self.inss) * self.quant #enquanto usarmos este meio de quantidade de pessoas na função usaremos esse quant aqui

        else:
            self.inss = self.salario * 0.15
            self.total = (self.salario + self.inss) * self.quant

        self.insereBanco()

    def insereBanco(self):
        conn = Banco.connect()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO pessoa (cargo, quant, salario, ferias, decimo, fgts, inss, total, categoria) 
        VALUES (?,?,?,?,?,?,?,?,?)
        """, (self.cargo, self.quant, self.salario, self.ferias, self.decimo, self.fgts, self.inss, self.total, self.categoria))

        cur.commit()
        conn.close()
