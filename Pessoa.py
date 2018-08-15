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

        if self.categoria != "labore":
            self.provFerias = (self.salario/12)*0.333333
            self.provdecimo = self.salario/12
            self.fgts = (self.salario + self.provFerias + self.provdecimo) * 0.08
            self.inss = (self.salario + self.provFerias + self.provdecimo) * 0.258
            self.total = (self.salario + self.provdecimo + self.provFerias + self.fgts + self.inss) * self.quant #enquanto usarmos este meio de quantidade de pessoas na função usaremos esse quant aqui

        else:
            self.inss = self.salario * 0.15
            self.total = (self.salario + self.inss) * self.quant

    def insereBanco(self):
        print
