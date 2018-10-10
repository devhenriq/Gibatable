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
from InvestimentoInicial import InvestimentoInicial
from InvestimentoFixo import InvestimentoFixo

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
        if ret == 'reserva':
            return rv

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

    def calculaPagRec(self, mes, var):

        if mes == " ":
            vtt = 0
            for mes in range(1,16):
                if var == 'Recebimentos':
                    fat = self.calculaFaturamento(mes)
                else:
                    fat = self.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes))
                avista = self.calculaTotal(CapGiro, 'avista', ' WHERE categoria = "' + var + '"')
                tres = self.calculaTotal(CapGiro, 'tres', ' WHERE categoria = "' + var + '"')
                seis = self.calculaTotal(CapGiro, 'seis', ' WHERE categoria = "' + var + '"')
                nove = self.calculaTotal(CapGiro, 'nov', ' WHERE categoria = "' + var + '"')
                total = avista + tres + seis + nove

                valv = fat * (avista / 100)
                valt = fat * (tres / 100)
                vals = fat * (seis / 100)
                valn = fat * (nove / 100)
                valtotal = valv + valt + vals + valn
                vtt += valtotal
        else:
            if var == 'Recebimentos':
                fat = self.calculaFaturamento(mes)
            else:
                fat = self.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes))
            avista = self.calculaTotal(CapGiro, 'avista', ' WHERE categoria = "' + var + '"')
            tres = self.calculaTotal(CapGiro, 'tres', ' WHERE categoria = "' + var + '"')
            seis = self.calculaTotal(CapGiro, 'seis', ' WHERE categoria = "' + var + '"')
            nove = self.calculaTotal(CapGiro, 'nov', ' WHERE categoria = "' + var + '"')
            total = avista + tres + seis + nove

            valv = fat * (avista / 100)
            valt = fat * (tres / 100)
            vals = fat * (seis / 100)
            valn = fat * (nove / 100)
            vtt = valv + valt + vals + valn

        return vtt

    def calculaMin(self, ret):
        receber = self.calculaPagRec(" ", 'Recebimentos')
        pagar = self.calculaPagRec(" ", 'Pagamentos')
        receita = self.calculaFaturamento(" ")
        canual = self.calculaTotal(Estoque, 'custototal')
        if receita != 0:
            pmrv = (receber / receita) * 360
        else:
            pmrv = 0
        if canual != 0:
            pmpc = (pagar / canual) * 360
        else:
            pmpc = 0
        pmre = (self.calculaTotal(Estoque, 'custototal', ' WHERE mes = 1') + self.calculaTotal(Estoque, 'custototal',
                                                                                             ' WHERE mes = 12') / 2) * 360
        if ret == 'pmrv':
            return pmrv
        if ret == 'pmpc':
            return pmpc
        if ret == 'pmre':
            return pmre

    def calculaInvPreOp(self):
        legal = self.calculaTotal(InvestimentoInicial, 'legalizacao')
        div = self.calculaTotal(InvestimentoInicial, 'divulgacao')
        out = self.calculaTotal(InvestimentoInicial, 'outros')
        return legal+div+out

    def necessidadeGiro(self, ret):
        receb = self.calculaMin('pmrv')
        est = self.calculaMin('pmre')
        sub = receb + est

        forn = self.calculaMin('pmpc')
        sub2 = forn
        liq = sub - sub2

        if ret == 'liq':
            return liq
        if ret == 'rec':
            return receb
        if ret == 'est':
            return est
        if ret == 'sub':
            return sub
        if ret == 'forn':
            return forn
        if ret == 'sub2':
            return sub2

    def caixaMin(self, ret):
        cf = self.calculaTotal(CustosFixos, 'total')
        cv = self.custosVariaveis(" ")/12
        ct = cf + cv
        ctd = ct/30
        need = self.necessidadeGiro('liq')
        total = need * ctd

        if ret == 'total':
            return total
        if ret == 'cf':
            return cf
        if ret == 'cv':
            return cv
        if ret == 'ct':
            return ct
        if ret == 'ctd':
            return ctd
        if ret == 'need':
            return need

    def capGiro(self):
        est = self.calculaTotal(Estoque, 'custototal')
        caixa = self.caixaMin('total')

        return est+caixa

    def balancoIni(self, ret):
        est = self.calculaTotal(InvestimentoInicial, 'estoque')
        caixa = self.calculaTotal(InvestimentoInicial, 'caixa')
        desp = self.calculaTotal(InvestimentoInicial, 'totaldesp')
        terr = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Imoveis Terrenos"')
        pred = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Imoveis Predios"')
        veic = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Fixos em Veiculos"')
        movs = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Moveis e Utensilios"')
        maqs = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Maquinas e Equipamentos"')
        comp = self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Computadores/Equipamentos de Informatica"')
        total = est + caixa + desp + terr + pred + veic + movs + maqs + comp
        forn = self.calculaPagRec(2, 'Pagamentos')+self.calculaPagRec(3, 'Pagamentos')+self.calculaPagRec(4, 'Pagamentos')
        emp = total - caixa - terr
        cap = self.calculaTotal(CapGiro, 'capsocial')
        totalp = forn + emp + cap
        outrosg = self.calculaTotal(InvestimentoInicial, 'outrosg')
        if ret == 'estoques':
            return est
        if ret == 'caixa':
            return caixa
        if ret == 'despesas':
            return desp
        if ret == 'terrenos':
            return terr
        if ret == 'predios':
            return pred
        if ret == 'veiculos':
            return veic
        if ret == 'moveis':
            return movs
        if ret == 'computador':
            return comp
        if ret == 'maquinas':
            return maqs
        if ret == 'totalativo':
            return total
        if ret == 'fornecedores':
            return forn
        if ret == 'emprestimos':
            return emp
        if ret == 'capsocial':
            return cap
        if ret == 'totalpassivo':
            return totalp
        if ret == 'outrosest':
            return outrosg

    def balancoProj(self, ret):

        terr = self.balancoIni('terrenos')
        pred = self.balancoIni('predios')
        deprimoveis = (self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Imoveis Predios"')*4)/100*(-1)

        veic = self.balancoIni('veiculos')
        mveic = (self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Fixos em Veiculos"')*20)/100*(-1)

        movs = self.balancoIni('moveis')
        mmovs = (self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Moveis e Utensilios"')*10)/100*(-1)

        comp = self.balancoIni('computadores')
        mcomp = (self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Computadores/Equipamentos de Informatica"')*20)/100*(-1)

        maqs = self.balancoIni('maquinas')
        mmaqs = (self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "Maquinas e Equipamentos"')*10)/100*(-1)


        desp = self.balancoIni('despesas')
        est = self.balancoIni('estoques')
        mdesp = desp/10*-1

        cli = 0
        for i in range(1,13):
            cli += self.calculaPagRec(i, 'Recebimentos')

        caixa = 0
        for i in range(1,13):
            caixa += self.calculaFaturamento(i)
            caixa -= self.custosVariaveis(i)
            caixa -= self.calculaTotal(CustosFixos, 'total')
            caixa += self.calculaPagRec(i)
            caixa -= self.calculaPagRec(i, 'Recebimentos')
            caixa += self.calculaPagRec(i, 'Pagamentos')

        caixa += self.balancoIni('caixa')
        caixa -= self.balancoIni('fornecedores')
        caixa -= mdesp
        caixa -= deprimoveis
        caixa -= mveic
        caixa -= mmovs
        caixa -= mcomp
        caixa -= mmaqs

        forn = self.balancoIni('fornecedores')

        irpj = 0
        for i in range(1,13):
            irpj += self.demonstrativo(i, 'irpj')

        emp = self.balancoIni('emprestimos')
        cap = self.balancoIni('capsocial')

        lucro = 0
        for i in range(1,13):
            lucro += self.demonstrativo('lucro')

        res = 0
        for i in range(1,13):
            res += self.demonstrativo('reserva')

        totala = caixa + cli + est + desp - mdesp + terr - deprimoveis + veic - mveic + movs - mmovs + comp - mcomp + maqs - mmaqs
        totalp = forn + irpj + emp + cap + lucro + res

        if ret == 'caixa':
            return caixa
        if ret == 'clientes':
            return cli
        if ret == 'estoques':
            return est
        if ret == 'despesas':
            return desp
        if ret == '-despesas':
            return mdesp
        if ret == 'terrenos':
            return terr
        if ret == 'predios':
            return pred
        if ret == '-imoveis':
            return deprimoveis
        if ret == 'veiculos':
            return veic
        if ret == '-veiculos':
            return mveic
        if ret == 'moveis':
            return movs
        if ret == '-moveis':
            return mmovs
        if ret == 'computadores':
            return comp
        if ret == '-computadores':
            return mcomp
        if ret == 'maquinas':
            return maqs
        if ret == '-maquinas':
            return mmaqs
        if ret == 'fornecedores':
            return forn
        if ret == 'irpj':
            return irpj
        if ret == 'emprestimos':
            return emp
        if ret == 'capsocial':
            return cap
        if ret == 'lucro':
            return lucro
        if ret == 'reservas':
            return res
        if ret == 'totalativo':
            return totala
        if ret == 'totalpassivo':
            return totalp