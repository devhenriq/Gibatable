from Banco import Banco

class Pessoa:

    def __init__(self, cargo, quant, salario, categoria):
        self.cargo = cargo
        self.quant = quant
        self.salario = salario
        self.categoria = categoria
        self.provferias = 0
        self.provdecimo = 0
        self.fgts = 0
        self.inss = 0
        self.total = None
        self.calculoPessoal()

    def calculoPessoal(self):

        if self.categoria != "Diretor":
            self.provferias = (self.salario/12)*0.333333
            self.provdecimo = self.salario/12
            self.fgts = (self.salario + self.provferias + self.provdecimo) * 0.08
            self.inss = (self.salario + self.provferias + self.provdecimo) * 0.258
            self.total = (self.salario + self.provdecimo + self.provferias + self.fgts + self.inss) * self.quant #enquanto usarmos este meio de quantidade de pessoas na função usaremos esse quant aqui

        else:
            self.inss = self.salario * 0.15
            self.total = (self.salario + self.inss) * self.quant
        self.insereBanco()

    def insereBanco(self):

        list = [self.cargo, self.quant, self.salario, self.provferias, self.provdecimo, self.fgts, self.inss, self.total, self.categoria]
        str = 'pessoa (cargo, quant, salario, ferias, decimo, fgts, inss, total, categoria)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'pessoa', col, cond)
        return ret