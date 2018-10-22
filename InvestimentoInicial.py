from Banco import Banco
from InvestimentoFixo import InvestimentoFixo
from Estoque import Estoque
from decimal import Decimal, ROUND_HALF_UP

class InvestimentoInicial:

    def __init__(self, invoutros, legal, divulg, outros, caixa, outrosg):
        self.totalfixo = 0
        self.movs = 0
        self.maqs = 0
        self.comps = 0
        self.veic = 0
        self.predios = 0
        self.terrenos = 0
        self.invoutros = invoutros
        self.totaldesp = 0
        self.legal = legal
        self.divulg = divulg
        self.outros = outros
        self.totalgiro = 0
        self.estoque = 0
        self.caixa = caixa
        self.outrosg = outrosg
        self.total = 0
        self.calcula()
        self.insereBanco()

    def calcula(self):
        self.movs = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Moveis e Utensilios'")
        self.maqs = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Maquinas e Equipamentos'")
        self.comps = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Computadores/Equipamentos de Informatica'")
        self.veic = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Fixos em Veiculos'")
        self.predios = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Imoveis Predios'")
        self.terrenos = self.preenche(InvestimentoFixo, "total", " WHERE categoria = 'Imoveis Terrenos'")
        self.totalfixo = float(Decimal(self.movs + self.maqs + self.comps + self.veic + self.predios + self.terrenos + self.invoutros).quantize(Decimal('0.01'),ROUND_HALF_UP))
        self.totaldesp = float(Decimal(self.legal + self.divulg).quantize(Decimal('0.01'),ROUND_HALF_UP))
        self.estoque = self.preenche(Estoque, "custototal") #total do estoque
        self.totalgiro = float(Decimal(self.estoque + self.caixa + self.outrosg).quantize(Decimal('0.01'),ROUND_HALF_UP))

        self.total = float(Decimal(self.totalfixo + self.totaldesp + self.totalgiro).quantize(Decimal('0.01'),ROUND_HALF_UP))


    def preenche(self, table=None, col=None, cond=None):

        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val

    def insereBanco(self):
        Banco.delete(Banco, 'investimentoinicial')
        list = [self.totalfixo, self.movs, self.maqs, self.comps, self.veic, self.predios, self.terrenos, self.invoutros,
                self.totaldesp, self.legal, self.divulg, self.outros, self.totalgiro, self.estoque, self.caixa, self.outrosg, self.total]
        strg = 'investimentoinicial (totalfixo, movs, maqs, comps, veic, predios, terrenos, invoutros, totaldesp, legalizacao, divulgacao, outros, totalgiro, estoque, caixa, outrosg, total)'
        deprec = self.calculaDeprec('totalmes') + ((self.legal + self.divulg + self.outros) / 12)
        deprec = self.dec(deprec)

        Banco.update(Banco, 'custosfixos', 'deprec =' + str(deprec))
        tt = self.calculaCF('maodeobra') + self.calculaCF('prolabore') + self.calculaCF('limpeza') + self.calculaCF('contador') + self.calculaCF('material') + self.calculaCF('agua') + self.calculaCF('aluguel') + self.calculaCF('manutencao') + deprec + self.calculaCF('outros')
        Banco.update(Banco, 'custosfixos', 'total =' + str(tt))
        Banco.insert(Banco, strg, list)

    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'investimentoinicial', col, cond)
        return ret

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val

    def calculaCF(self, col=None, cond=None):
        list = Banco.relatorio(Banco, 'custosfixos', col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val

    def dec(self, val):
        v = float(Decimal(val).quantize(Decimal('0.01'),ROUND_HALF_UP))
        return v

    def calculaDeprec(self, ret):
        contas = ['Moveis e Utensilios', 'Maquinas e Equipamentos', 'Computadores/Equipamentos de Informatica',
                  'Fixos em Veiculos', 'Imoveis Predios', 'Imoveis Terrenos']
        total = 0
        totalmes = 0

        for t in contas:

            valor = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "' + t + '"')

            if t == 'Moveis e Utensilios' or t == 'Maquinas e Equipamentos':
                taxa = 10
            else:
                if t == 'Computadores/Equipamentos de Informatica' or t == 'Fixos em Veiculos':
                    taxa = 20
                else:
                    if t == 'Imoveis Predios':
                        taxa = 4
                    else:
                        taxa = 0

            mensal = float(Decimal(((valor * taxa) / 100) / 12).quantize(Decimal('0.01'), ROUND_HALF_UP))
            total = float(Decimal(total + valor).quantize(Decimal('0.01'), ROUND_HALF_UP))
            totalmes = float(Decimal(totalmes + mensal).quantize(Decimal('0.01'), ROUND_HALF_UP))

        if ret == 'total':
            return total
        if ret == 'totalmes':
            return totalmes
