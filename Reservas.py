from Banco import Banco

class Reservas:
    def __init__(self,cs, rsv):
        self.capsocial = cs
        self.reservas = rsv

        Banco.delete(Banco, 'reservas')
        self.insereBanco()


    def insereBanco(self):
        list = [self.reservas, self.capsocial]
        str = 'reservas(reservas, capsocial)'
        Banco.insert(Banco, str, list)



    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'reservas', col, cond)
        return ret