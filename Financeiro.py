from MateriaPrima import MateriaPrima
from Estimativa import Estimativa
from Pessoa import Pessoa
from RateioOp import RateioOp
from RateioFixos import RateioFixos
from CustosFixos import CustosFixos
from PrecoVenda import PrecoVenda
from CustoFinanceiroMensal import CustoFinanceiroMensal
from CustoVendas import CustoVendas
from Tributos import Tributos
from Frete import Frete
from Estoque import Estoque
from CapGiro import CapGiro

class Financeiro:
    def demonstrativo(self, mes, ret):
        fat = self.calculaFaturamento(mes)
        cv = self.custosVariaveis(mes)
        mc = fat - cv
        cf = self.calculaTotal(CustosFixos, 'total')

        lucro = mc - cf

        ipr = lucro * (self.calculaTotal(Tributos, 'irpj') / 100)

        reserv = self.calculaTotal(CapGiro, 'reservas')
        rv = (lucro * reserv) / 100
        liquido = lucro - ipr - rv

        if ret == 'liquido':
            return liquido
        if ret == 'imposto':
            return ipr

    def calculaFaturamento(self, mes):
        produtos = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        fat = 0
        for prod in produtos:
            if mes == " ":
                est = self.calculaTotal(Estimativa, 'DISTINCT quant',
                                        ' WHERE descricao = "' + prod[0] + '"')
            else:
                est = self.calculaTotal(Estimativa, 'DISTINCT quant',
                                        ' WHERE mes = ' + str(mes) + ' AND descricao = "' + prod[0] + '"')
            pv = self.calculaPV(prod[0], mes, 'Preco')
            val = est * pv
            fat += val
        return fat

    def calculaPV(self, nome, mes, retorno):
        mat = self.calculaTotal(MateriaPrima, 'total', ' WHERE produto = "' + nome + '"')

        total = self.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')
        rateio = self.calculaTotal(RateioOp, 'porc', ' WHERE produto = "' + nome + '"')
        op = total * (rateio / 100)
        quant = self.calculaTotal(Estimativa, 'quant', ' WHERE descricao = "' + nome + '"')
        if quant != 0:
            cprod = op / quant
        else:
            cprod = 0

        total = self.calculaTotal(CustosFixos, 'total')
        rateio = self.calculaTotal(RateioFixos, 'porc', ' WHERE produto = "' + nome + '"')
        op = total * (rateio / 100)
        quant = self.calculaTotal(Estimativa, 'quant', ' WHERE descricao = "' + nome + '"')
        if quant != 0:
            cfixo = op / quant
        else:
            cfixo = 0
        if mes == " ":
            outros = self.calculaTotal(PrecoVenda, 'outros',
                                       ' WHERE produto = "' + nome + '"')
        else:
            outros = self.calculaTotal(PrecoVenda, 'outros',
                                       ' WHERE mes =' + str(mes) + ' AND produto = "' + nome + '"')

        cip = mat + cprod + outros

        if mes == " ":
            if self.calculaTotal(Estimativa, 'quant') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * self.calculaTotal(CustoFinanceiroMensal,
                                                                                                'invest')) / self.calculaTotal(
                    Estimativa, 'quant')
            else:
                cfgiro = 0
        else:
            if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * self.calculaTotal(CustoFinanceiroMensal,
                                                                                                'invest')) / self.calculaTotal(
                    Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"')
            else:
                cfgiro = 0

        lucro = self.calculaTotal(Estimativa, 'lucrounitario', ' WHERE descricao = "' + nome + '"')

        trib = self.calculaTotal(Tributos, 'total') * 0.01
        cvenda = self.calculaTotal(CustoVendas, 'porcentagem') * 0.01
        preco = (cip + cfixo + lucro + cfgiro) * (1 / (1 - (trib + cvenda)))

        ctrib = preco * trib
        cdirvendas = preco * cvenda

        ctotal = cip + ctrib + cdirvendas

        if retorno == 'Preco':
            return preco

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val

    def custosVariaveis(self, mes):

        pd = self.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')

        trib = self.calculaTotal(Tributos, 'total')
        ct = self.calculaFaturamento(mes)
        imp = ct * trib

        cv = self.calculaTotal(CustoVendas, 'porcentagem')
        cvendas = ct * cv

        if mes == " ":
            etq = self.calculaTotal(Estoque, 'custototal')

            frete = self.calculaTotal(Frete, 'frete')

            pj = Estimativa.relatorio(Estimativa, 'DISTINCT quant')

            opv = PrecoVenda.relatorio(PrecoVenda, 'outros')
        else:
            etq = self.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes))

            frete = self.calculaTotal(Frete, 'frete', ' WHERE mes = ' + str(mes))

            pj = Estimativa.relatorio(Estimativa, 'DISTINCT quant',
                                      ' WHERE mes = ' + str(mes))

            opv = PrecoVenda.relatorio(PrecoVenda, 'outros', ' WHERE mes = ' + str(mes))
        ter = 0
        for outros in opv:
            for proj in pj:
                ter += proj[0] * outros[0]

        inv = self.calculaTotal(CustoFinanceiroMensal, 'invest')
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo

        cvar = pd + imp + cvendas + etq + frete + ter + amort

        return cvar