from Banco import Banco

class CustoVendas:

    def __init__(self, desc, porc):
        self.descricao = desc
        self.porc = porc
        self.indice = porc/100

        self.insereBanco()

    def insereBanco(self):
        list = [self.descricao, self.porc, self.indice]
        str = "custovendas (descricao, porcentagem, indice)"
        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'custovendas', col, cond)
        return ret