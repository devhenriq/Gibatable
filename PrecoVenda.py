from Banco import Banco

class PrecoVenda:

    def __init__(self, outros, mes):
        self.outros = outros
        self.mes = mes
        self.insereBanco()

    def insereBanco(self):
        list = [self.mes, self.outros]
        str = 'precovenda (mes, outros)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col=None, cond=None):
        return Banco.relatorio(Banco, 'precovenda')