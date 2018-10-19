from Banco import Banco

class PrecoVenda:

    def __init__(self,produto, outros, mes):
        self.prod = produto
        self.outros = outros
        self.mes = mes
        self.insereBanco()

    def insereBanco(self):
        list = [self.prod, self.mes, self.outros]
        str = 'precovenda (produto, mes, outros)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col=None, cond=None):
        return Banco.relatorio(Banco, 'precovenda', col, cond)