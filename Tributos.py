from Banco import Banco

class Tributos:

    def __init__(self, simples = None, icms = None, pis = None, cofins = None, ipi = None, iss = None, irpj = None):
        self.simples = simples
        self.icms = icms
        self.pis = pis
        self.cofins = cofins
        self.ipi = ipi
        self.iss = iss
        self.irpj = irpj
        self.total = simples + icms + pis + cofins + ipi + iss + irpj
        self.insereBanco()

    def insereBanco(self):

        list = [self.simples, self.icms, self.pis, self.cofins, self.ipi, self.iss, self.irpj, self.total]
        str = 'tributos (simples, icms, pis, cofins, ipi, iss, irpj, total)'


        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'tributos', col, cond)
        return ret