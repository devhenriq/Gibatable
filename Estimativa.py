class Estimativa:

    def __init__(self, descricao, quant, lucro, mes):
        self.descricao = descricao
        self.quant = quant
        self.lucro = lucro
        self.lucrott = quant * lucro
        self.mes = mes

    def insereBanco(self):
        print