from Banco import Banco

class RateioFixos:
    def __init__(self, list):
        self.produto = list[0].text
        self.porc = list[1].text
        self.insereBanco()

    def insereBanco(self):
        list = [self.produto, self.porc]
        str = 'rateiocustosfixos (produto, porc)'

        Banco.delete(Banco, 'rateiocustosfixos')
        Banco.insert(Banco, str, list)

    def relatorio(self, col=None, cond=None):
        return Banco.relatorio(Banco, 'rateiocustosfixos', col, cond)