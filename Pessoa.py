from Banco import Banco
from decimal import Decimal, ROUND_HALF_UP

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
            self.provferias = float(Decimal((self.salario/12)*0.333333).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.provdecimo = float(Decimal((self.salario/12)).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.fgts = float(Decimal((self.salario + self.provferias + self.provdecimo) * 0.08).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.inss = float(Decimal((self.salario + float(self.provferias) + self.provdecimo) * 0.258).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.total = float(Decimal((self.salario + float(self.provferias) + self.provdecimo + self.fgts + self.inss) * self.quant).quantize(Decimal('0.01'), ROUND_HALF_UP)) #enquanto usarmos este meio de quantidade de pessoas na função usaremos esse quant aqui

        else:
            self.inss = float(Decimal(self.salario * 0.15).quantize(Decimal('0.01'), ROUND_HALF_UP))
            self.total = float(Decimal((self.salario + self.inss) * self.quant).quantize(Decimal('0.01'), ROUND_HALF_UP))
        self.insereBanco()

    def insereBanco(self):

        list = [self.cargo, self.quant, self.salario, self.provferias, self.provdecimo, self.fgts, self.inss, self.total, self.categoria]
        str = 'pessoa (cargo, quant, salario, ferias, decimo, fgts, inss, total, categoria)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'pessoa', col, cond)
        return ret