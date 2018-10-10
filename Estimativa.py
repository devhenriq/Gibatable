from Banco import Banco
from decimal import Decimal, ROUND_HALF_UP
class Estimativa:

    def __init__(self, descricao, quant, lucro, mes):
        self.descricao = descricao
        self.quant = quant
        self.lucro = lucro
        self.lucrott = float(Decimal(quant * lucro).quantize(Decimal('0.01'),ROUND_HALF_UP))
        self.mes = mes
        self.insereBanco()

    def insereBanco(self):
        list = [self.descricao, self.quant, self.lucro, self.mes, self.lucrott]
        str = 'estimativa(descricao, quant, lucrounitario, mes, lucrototal)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'estimativa', col, cond)
        return ret