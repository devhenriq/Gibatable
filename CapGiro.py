from Banco import Banco

class CapGiro:
    def __init__(self, fat, pag, cs, rsv, cat):
        self.vista = fat
        self.tres = pag
        self.seis = cs
        self.nove = rsv
        self.categoria = cat

        Banco.delete(Banco, 'capgiro', None, ' WHERE categoria = "' + cat + '"')
        self.insereBanco()


    def insereBanco(self):
        list = [self.vista, self.tres, self.seis, self.nove, self.categoria]
        str = 'capgiro(avista, tres, seis, nov, categoria)'
        Banco.insert(Banco, str, list)



    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'capgiro', col, cond)
        return ret