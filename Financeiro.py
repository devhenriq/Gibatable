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
from decimal import Decimal, ROUND_HALF_UP
class Financeiro:
    def dec(self, var):
        return float(Decimal(var).quantize(Decimal('0.01'), ROUND_HALF_UP))

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
            return self.dec(liquido)
        if ret == 'imposto':
            return self.dec(ipr)
        if ret == 'reserva':
            return self.dec(rv)

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
        return float(Decimal(fat).quantize(Decimal('0.01', ROUND_HALF_UP)))

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
            return float(Decimal(preco).quantize(Decimal('0.01', ROUND_HALF_UP)))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return float(Decimal(val).quantize(Decimal('0.01', ROUND_HALF_UP)))

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

        return self.dec(cvar)

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

        return self.dec(vtt)

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
            return self.dec(pmrv)
        if ret == 'pmpc':
            return self.dec(pmpc)
        if ret == 'pmre':
            return self.dec(pmre)

    def calculaInvPreOp(self):
        legal = self.calculaTotal(InvestimentoInicial, 'legalizacao')
        div = self.calculaTotal(InvestimentoInicial, 'divulgacao')
        out = self.calculaTotal(InvestimentoInicial, 'outros')
        return self.dec(legal+div+out)

    def necessidadeGiro(self, ret):
        receb = self.calculaMin('pmrv')
        est = self.calculaMin('pmre')
        sub = receb + est

        forn = self.calculaMin('pmpc')
        sub2 = forn
        liq = sub - sub2

        if ret == 'liq':
            return self.dec(liq)
        if ret == 'rec':
            return self.dec(receb)
        if ret == 'est':
            return self.dec(est)
        if ret == 'sub':
            return self.dec(sub)
        if ret == 'forn':
            return self.dec(forn)
        if ret == 'sub2':
            return self.dec(sub2)

    def caixaMin(self, ret):
        cf = self.calculaTotal(CustosFixos, 'total')
        cv = self.custosVariaveis(" ")/12
        ct = cf + cv
        ctd = ct/30
        need = self.necessidadeGiro('liq')
        total = need * ctd

        if ret == 'total':
            return self.dec(total)
        if ret == 'cf':
            return self.dec(cf)
        if ret == 'cv':
            return self.dec(cv)
        if ret == 'ct':
            return self.dec(ct)
        if ret == 'ctd':
            return self.dec(ctd)
        if ret == 'need':
            return self.dec(need)

    def capGiro(self):
        est = self.calculaTotal(Estoque, 'custototal')
        caixa = self.caixaMin('total')

        return self.dec(est+caixa)

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
            return self.calculaMin(est)
        if ret == 'caixa':
            return self.calculaMin(caixa)
        if ret == 'despesas':
            return self.calculaMin(desp)
        if ret == 'terrenos':
            return self.calculaMin(terr)
        if ret == 'predios':
            return self.calculaMin(pred)
        if ret == 'veiculos':
            return self.calculaMin(veic)
        if ret == 'moveis':
            return self.calculaMin(movs)
        if ret == 'computador':
            return self.calculaMin(comp)
        if ret == 'maquinas':
            return self.calculaMin(maqs)
        if ret == 'totalativo':
            return self.calculaMin(total)
        if ret == 'fornecedores':
            return self.calculaMin(forn)
        if ret == 'emprestimos':
            return self.calculaMin(emp)
        if ret == 'capsocial':
            return self.calculaMin(cap)
        if ret == 'totalpassivo':
            return self.calculaMin(totalp)
        if ret == 'outrosest':
            return self.calculaMin(outrosg)

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
            return self.calculaMin(caixa)
        if ret == 'clientes':
            return self.calculaMin(cli)
        if ret == 'estoques':
            return self.calculaMin(est)
        if ret == 'despesas':
            return self.calculaMin(desp)
        if ret == '-despesas':
            return self.calculaMin(mdesp)
        if ret == 'terrenos':
            return self.calculaMin(terr)
        if ret == 'predios':
            return self.calculaMin(pred)
        if ret == '-imoveis':
            return self.calculaMin(deprimoveis)
        if ret == 'veiculos':
            return self.calculaMin(veic)
        if ret == '-veiculos':
            return self.calculaMin(mveic)
        if ret == 'moveis':
            return self.calculaMin(movs)
        if ret == '-moveis':
            return self.calculaMin(mmovs)
        if ret == 'computadores':
            return self.calculaMin(comp)
        if ret == '-computadores':
            return self.calculaMin(mcomp)
        if ret == 'maquinas':
            return self.calculaMin(maqs)
        if ret == '-maquinas':
            return self.calculaMin(mmaqs)
        if ret == 'fornecedores':
            return self.calculaMin(forn)
        if ret == 'irpj':
            return self.calculaMin(irpj)
        if ret == 'emprestimos':
            return self.calculaMin(emp)
        if ret == 'capsocial':
            return self.calculaMin(cap)
        if ret == 'lucro':
            return self.calculaMin(lucro)
        if ret == 'reservas':
            return self.calculaMin(res)
        if ret == 'totalativo':
            return self.calculaMin(totala)
        if ret == 'totalpassivo':
            return self.calculaMin(totalp)

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
            return self.dec(total)
        if ret == 'totalmes':
            return self.dec(totalmes)