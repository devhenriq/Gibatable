from Banco import Banco

class InvestimentoFixo:

    def __init__(self, descricao, quant, valorUnit, categoria):
        self.descr = descricao
        self.quant = quant
        self.valorUnit = valorUnit
        self.valorTotal = valorUnit * quant
        self.categoria = categoria
        self.insereBanco()

    def insereBanco(self):
        list = [self.descr, self.quant, self.valorUnit, self.valorTotal, self.categoria]
        str = 'investimentofixo (descricao, quant, valorunitario, total, categoria)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'investimentofixo', col, cond)
        return ret