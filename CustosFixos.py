from Banco import Banco
from Pessoa import Pessoa
from InvestimentoFixo import InvestimentoFixo
from decimal import Decimal, ROUND_HALF_UP
from InvestimentoInicial import InvestimentoInicial
class CustosFixos:

    def __init__(self, limpeza, cont, mat, agua, aluguel, manutencao, outros):
        self.adm = 0
        self.dir = 0
        self.limpeza = limpeza
        self.cont = cont
        self.mat = mat
        self.agua = agua
        self.aluguel = aluguel
        self.manutencao = manutencao
        self.deprec = 0
        self.outros = outros
        self.calcula()

    def calcula(self):

        list = Pessoa.relatorio(Pessoa, "total", " WHERE categoria = 'Administrativo'")

        if list is not None:
            for t in list:
                t = str(t).replace(",","").replace(")","").replace("(","")
                self.adm = self.adm + float(t)

        list = Pessoa.relatorio(Pessoa, "total"," WHERE categoria = 'Diretor'")

        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")","").replace("(","")
                self.dir = self.dir + float(t)

        self.deprec = self.calculaDeprec('totalmes') + ((self.calculaTotal(InvestimentoInicial, 'legalizacao') + self.calculaTotal(InvestimentoInicial, 'divulgacao') + self.calculaTotal(InvestimentoInicial, 'outros'))/12)
        self.deprec = float(Decimal(self.deprec).quantize(Decimal('0.01'), ROUND_HALF_UP))
        Banco.delete(Banco, 'custosfixos')
        self.total = self.adm + self.dir + self.limpeza + self.cont + self.mat + self.agua + self.aluguel + self.manutencao + self.deprec + self.outros
        self.insereBanco()


    def insereBanco(self):
        list = [self.adm, self.dir, self.limpeza, self.cont, self.mat, self.agua, self.aluguel, self.manutencao, self.deprec, self.outros, self.total]
        str = 'custosfixos (maodeobra, prolabore, limpeza, contador, material, agua, aluguel, manutencao, deprec, outros, total)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'custosfixos', col, cond)
        return ret

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

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val