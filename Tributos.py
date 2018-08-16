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

    def insereBanco(self):
        print

