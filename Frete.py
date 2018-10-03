from Banco import Banco

class Frete:
    def __init__(self, frete, mes):
        self.frete = frete
        self.mes = mes
        Banco.delete(Banco, 'progfin')
        self.insereBanco()


    def insereBanco(self):
        list = [self.frete, self.mes]
        str = 'progfin(frete, mes)'
        Banco.insert(Banco, str, list)


    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'progfin', col, cond)
        return ret