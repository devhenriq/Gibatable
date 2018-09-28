from Banco import Banco
from MateriaPrima import MateriaPrima
from Estimativa import Estimativa

class Estoque:

    def __init__(self):

        list = Estimativa.relatorio('estimativa')
        if list is not None:
            for e in list:
                self.descr = e[0]
                self.quant = e[1]
                self.custounit = self.calculaTotal(MateriaPrima, 'total', " WHERE produto = '" + str(self.descr)+ "'")
                self.custototal = self.quant * self.custounit
                self.mes = e[3]
                #Banco.delete(Banco, 'estoque')
                self.insereBanco()

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


    def insereBanco(self):
        str = 'estoque(descricao, quant, custounit, custototal, mes)'
        list = [self.descr, self.quant, self.custounit, self.custototal, self.mes]
        Banco.insert(Banco, str, list)


    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'estoque', col, cond)
        return ret