from Banco import Banco

class CapGiro:
    def __init__(self, fat, pag, cs, rsv):
        self.faturamento = fat
        self.pagamento = pag
        self.capsocial = cs
        self.reservas = rsv
        Banco.delete(Banco, 'capgiro')
        self.insereBanco()


    def insereBanco(self):
        list = [self.faturamento, self.pagamento, self.capsocial, self.reservas]
        str = 'capgiro(faturamento, pagamento, capsocial, reservas)'
        Banco.insert(Banco, str, list)



    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'capgiro', col, cond)
        return ret