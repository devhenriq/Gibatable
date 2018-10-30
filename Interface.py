from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from os import listdir
from Reservas import Reservas
from Pessoa import Pessoa
from InvestimentoFixo import InvestimentoFixo
from MateriaPrima import MateriaPrima
from Estimativa import Estimativa
from CustosFixos import CustosFixos
from Tributos import Tributos
from CustoVendas import CustoVendas
from InvestimentoInicial import InvestimentoInicial
from Estoque import Estoque
from CustoFinanceiroMensal import CustoFinanceiroMensal
from RateioOp import RateioOp
from RateioFixos import RateioFixos
from PrecoVenda import PrecoVenda
from Frete import Frete
from CapGiro import CapGiro
from kivy.clock import mainthread
from kivy.uix.spinner import Spinner
import gc
from Financeiro import *
from decimal import Decimal, ROUND_HALF_UP
from Banco import Banco

Window.fullscreen = False
Config.set('graphics', 'resizable', True)
Config.write()

# Manager
class Manager(ScreenManager):
    pass

# Telas
class MenuScreen(Screen):
    pass


class StartScreen(Screen):
    pass


class CadastroScreen(Screen):
    pass

# Cadastro
class PessoaScreen(Screen):
    def envia(self):
        p = Pessoa(self.cargo.text, int(self.quant.text), float(self.salario.text), self.categoria.text)
        p.relatorio()
        self.cargo.text = ""
        self.quant.text = ""
        self.salario.text = ""
        self.categoria.text = "-"


class InvestimentoScreen(Screen):
    def envia(self):
        i = InvestimentoFixo(self.descr.text, int(self.quant.text), float(self.vunit.text), self.categoria.text)
        i.relatorio()
        self.descr.text = ""
        self.quant.text = ""
        self.vunit.text = ""
        self.categoria.text = "-"


class MateriaPrimaScreen(Screen):
    def envia(self):
        m = MateriaPrima(self.nome.text, self.materia.text, self.medida.text, float(self.preco.text), float(self.quant.text))
        m.relatorio()
        # self.nome.text = ""
        # self.materia.text = ""
        # self.medida.text = ""
        # self.preco.text = ""
        # self.quant.text = ""


class PreEstimativaScreen(Screen):
    pass


class EstimativaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Escolha o produto:'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(CadastroBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        for prod in dados:
            for mp in prod:
                self.criabotao(mp)

    def criabotao(self, nome):
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.preenche(nome))
        self.scrl.add_widget(bt)

    def preenche(self, nome):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Estimativa de Vendas'
        self.back.clear_widgets()


        self.scrl.add_widget(Label(text='Quantidade: '))
        tx1 = TextInput()
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text='Lucro Unitario: '))
        tx2 = TextInput()
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text='Mes: '))
        tx3 = Spinner(values=('1','2','3','4','5','6','7','8','9','10','11','12'))
        self.scrl.add_widget(tx3)

        self.back.add_widget(Button(text="Enviar", on_release=lambda x: self.envia(nome, tx1,tx2,tx3)))
        self.back.add_widget(CadastroBt())

    def envia(self, nome, quant, lucro, mes):
        e = Estimativa(nome, int(quant.text), float(lucro.text), mes.text)
        e.relatorio()
        # self.descr.text = ""
        # self.quant.text = ""
        # self.lucro.text = ""
        Estoque(nome, mes.text)


class CustosFixosScreen(Screen):
    def envia(self):
        c = CustosFixos(float(self.limp.text), float(self.cont.text), float(self.mat.text), float(self.agua.text), float(self.aluguel.text), float(self.man.text), float(self.outros.text))
        c.relatorio()
        self.limp.text = ""
        self.cont.text = ""
        self.mat.text = ""
        self.agua.text = ""
        self.aluguel.text = ""
        self.man.text = ""
        self.outros.text = ""


class ReservasScreen(Screen):
    def envia(self):
        pv = Reservas(self.capsocial.text, self.res.text)
        pv.relatorio()


class TributosScreen(Screen):
    def envia(self):
        t = Tributos(float(self.simples.text), float(self.icms.text), float(self.pis.text), float(self.cofins.text), float(self.ipi.text), float(self.iss.text), float(self.irpj.text))
        t.relatorio()
        self.simples.text = ""
        self.icms.text = ""
        self.pis.text = ""
        self.cofins.text = ""
        self.ipi.text = ""
        self.iss.text = ""
        self.irpj.text = ""


class CustoVendasScreen(Screen):
    def envia(self):
        cv = CustoVendas(self.descricao.text, float(self.porc.text))
        cv.relatorio()
        self.descricao.text = ""
        self.porc.text = ""


class InvestimentoInicialScreen(Screen):
    def envia(self):
        ii = InvestimentoInicial(float(self.invoutros.text), float(self.legal.text), float(self.divulg.text), float(self.outros.text), float(self.caixa.text), float(self.outrosg.text))
        ii.relatorio()
        self.invoutros.text = ""
        self.legal.text = ""
        self.divulg.text = ""
        self.outros.text = ""
        self.caixa.text = ""
        self.outrosg.text = ""


class CustoFinanceiroMensalScreen(Screen):
    def envia(self):
        cfm = CustoFinanceiroMensal(float(self.custo.text))
        cfm.relatorio()
        self.custo.text = ""


class RateioCustosFixosScreen(Screen):
    inputs = []

    def envia(self):
        for w in self.inputs:
            rto = RateioFixos(w) #adicionar na lista os inputs criado na linha 160 dos text input. (15 linhas abaixo)k
            rto.relatorio()

    @mainthread
    def on_enter(self):
        for w in self.inputs:
            w[0].canvas.clear()
            w[1].canvas.clear()
            w[2].canvas.clear()

        list = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        self.scrl.clear_widgets()
        x = 0
        for e in list:
            lista = []

            label = Label(text=e[0])
            self.scrl.add_widget(label)
            lista.append(label)

            tx = RateioFixos.relatorio(RateioFixos, 'porc', ' WHERE produto = "' + str(e[0])+ '"')
            print(tx)
            if tx.count(tx) is not 0:
                textin = TextInput(text=str(tx[0][0]),font_size=32,multiline=False)
            else:
                textin = TextInput(font_size=32, multiline=False)
            self.scrl.add_widget(textin)
            lista.append(textin)

            label2 = Label(text='%')
            self.scrl.add_widget(label2)
            lista.append(label2)

            self.inputs.append(lista)
            x = x + 1
        #self.add_widget(scrollview)


class RateioCustosOpScreen(Screen):
    inputs = []

    def envia(self):
        for w in self.inputs:
            rto = RateioOp(w)  # adicionar na lista os inputs criado na linha 160 dos text input. (15 linhas abaixo)k
            rto.relatorio()

    @mainthread
    def on_enter(self):
        for w in self.inputs:
            w[0].canvas.clear()
            w[1].canvas.clear()
            w[2].canvas.clear()

        list = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        x = 0
        for e in list:
            lista = []

            label = Label(text=e[0])
            self.scrl.add_widget(label)
            lista.append(label)

            tx = RateioOp.relatorio(RateioOp, 'porc', ' WHERE produto = "' + str(e[0])+'"')
            if tx.count(tx) is not 0:
                textin = TextInput(text=str(tx[0][0]),font_size=32,multiline=False)
            else:
                textin = TextInput(font_size=32, multiline=False)
            self.scrl.add_widget(textin)
            lista.append(textin)

            label2 = Label(text='%')
            self.scrl.add_widget(label2)
            lista.append(label2)

            self.inputs.append(lista)
            x = x + 1


class PrecoVendaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de Venda'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(CadastroBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        for prod in dados:
            for mp in prod:
                self.criabotao(mp)

    def criabotao(self, nome):
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.preenche(nome))
        self.scrl.add_widget(bt)

    def preenche(self, nome):
        print(nome)
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = nome
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Outros custos'))
        tx1 = TextInput()
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Mes'))
        tx2 = Spinner(values=('1','2','3','4','5','6','7','8','9','10','11','12'))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=''))


        self.back.add_widget(SendButton(on_release=lambda x: (self.envia(tx1.text, tx2.text, nome))))
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def envia(self, val, mes, prod):
        Banco.delete(Banco, 'precovenda', None, ' WHERE produto = "' + prod + '"' + ' AND mes = '+ mes)
        pv = PrecoVenda(prod, val, mes)
        p = pv.relatorio()
        print(p)

class FinFreteScreen(Screen):
    def envia(self):
        pv = FinFreteScreen(self.frete.text, self.mes.text)
        pv.relatorio()


class CapGiroScreen(Screen):
    def envia(self):
        pv = CapGiro(self.avista.text, self.tres.text, self.seis.text, self.nov.text, self.categoria.text)
        pv.relatorio()


#Relatorios
class RelatorioScreen(Screen):
    pass

class RelatoriosCustosScreen(Screen):
    pass


class RelatoriosFinScreen(Screen):
    pass


class RelGiroScreen(Screen):
    pass


#Pessoas
class RelPessoaScreen(Screen):
    pass


class RelPessoaDirScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = Pessoa.relatorio(Pessoa, 'cargo, quant, salario, inss, total', ' WHERE categoria="Diretor"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text = '')
        self.scrl.add_widget(label)
        label = Label(text = 'Cargo')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Salario')
        self.scrl.add_widget(label)
        label = Label(text='INSS')
        self.scrl.add_widget(label)
        label = Label(text='Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d,str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4*self.height, size_hint=[1,1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=str(int(Decimal(self.calculaTotal(Pessoa, 'quant', ' WHERE categoria="Diretor"')).quantize(Decimal('0.01'),ROUND_HALF_UP)))))
        self.scrl.add_widget(Label(text="%.2f" %float(Decimal(self.calculaTotal(Pessoa, 'salario', ' WHERE categoria="Diretor"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" %float(Decimal(self.calculaTotal(Pessoa, 'inss', ' WHERE categoria="Diretor"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" %float(Decimal(self.calculaTotal(Pessoa, 'total', ' WHERE categoria="Diretor"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


class RelPessoaOpScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = Pessoa.relatorio(Pessoa, 'cargo, quant, salario, ferias, decimo, fgts, inss, total', ' WHERE categoria="Producao"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text = '')
        self.scrl.add_widget(label)
        label = Label(text = 'Cargo')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Salario')
        self.scrl.add_widget(label)
        label = Label(text='Ferias')
        self.scrl.add_widget(label)
        label = Label(text='Decimo Terceiro')
        self.scrl.add_widget(label)
        label = Label(text='FGTS')
        self.scrl.add_widget(label)
        label = Label(text='INSS')
        self.scrl.add_widget(label)
        label = Label(text='Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d,str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4*self.height, size_hint=[1,1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=str(int(self.calculaTotal(Pessoa, 'quant', ' WHERE categoria="Producao"')))))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'salario', ' WHERE categoria="Producao"')))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'ferias', ' WHERE categoria="Producao"')))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'decimo', ' WHERE categoria="Producao"')))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'fgts', ' WHERE categoria="Producao"')))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'inss', ' WHERE categoria="Producao"')))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Pessoa, 'total', ' WHERE categoria="Producao"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


class RelPessoaAdmScreen(Screen):
    labels = []
    @mainthread
    def on_enter(self):
        dados = Pessoa.relatorio(Pessoa, 'cargo, quant, salario, ferias, decimo, fgts, inss, total', ' WHERE categoria="Administrativo"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text = '')
        self.scrl.add_widget(label)
        label = Label(text = 'Cargo')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Salario')
        self.scrl.add_widget(label)
        label = Label(text='Ferias')
        self.scrl.add_widget(label)
        label = Label(text='Decimo Terceiro')
        self.scrl.add_widget(label)
        label = Label(text='FGTS')
        self.scrl.add_widget(label)
        label = Label(text='INSS')
        self.scrl.add_widget(label)
        label = Label(text='Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d,str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4*self.height, size_hint=[1,1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=str(int(Decimal(self.calculaTotal(Pessoa, 'quant', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP)))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'salario', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'ferias', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'decimo', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'fgts', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'inss', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))
        self.scrl.add_widget(Label(text="%.2f" % float(Decimal(self.calculaTotal(Pessoa, 'total', ' WHERE categoria="Administrativo"')).quantize(Decimal('0.01'),ROUND_HALF_UP))))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str(val)


#Investimentos Fixos e Depreciaçoes
class RelInvFixoScreen(Screen):
    pass


class RelCompScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total', ' WHERE categoria="Computadores/Equipamentos de Informatica"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text = '')
        self.scrl.add_widget(label)
        label = Label(text = 'Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d,str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str('%.2f' % d), font_size=0.4*self.height, size_hint=[1,1])
                    else:
                        label = Label(text="%.2f" % float(Decimal(d).quantize(Decimal('0.01'), ROUND_HALF_UP)), font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria="Computadores/Equipamentos de Informatica"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


class RelDeprecScreen(Screen):

    @mainthread
    def on_enter(self):
        contas = ['Moveis e Utensilios', 'Maquinas e Equipamentos', 'Computadores/Equipamentos de Informatica', 'Fixos em Veiculos', 'Imoveis Predios', 'Imoveis Terrenos']
        total = 0
        totalmes = 0

        self.scrl.clear_widgets()
        gc.collect()


        label = Label(text='Conta')
        self.scrl.add_widget(label)
        label = Label(text='Valor aquisicao')
        self.scrl.add_widget(label)
        label = Label(text='Taxa anual')
        self.scrl.add_widget(label)
        label = Label(text='Valor mensal')
        self.scrl.add_widget(label)

        for t in contas:

            label = Label(text=t)
            self.scrl.add_widget(label)

            valor=self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria = "' + t + '"')
            label = Label(text=str("%.2f" % valor))
            self.scrl.add_widget(label)

            if t == 'Moveis e Utensilios' or t == 'Maquinas e Equipamentos':
                taxa = 10
            else:
                if t == 'Computadores/Equipamentos de Informatica' or t == 'Fixos em Veiculos':
                    taxa = 20
                else:
                    if  t == 'Imoveis Predios':
                        taxa = 4
                    else:
                        taxa = 0

            label = Label(text=str(taxa))
            self.scrl.add_widget(label)

            mensal = float(Decimal(((valor*taxa)/100)/12).quantize(Decimal('0.01'),ROUND_HALF_UP))
            label = Label(text=str("%.2f" % mensal))
            self.scrl.add_widget(label)

            total = float(Decimal(total + valor).quantize(Decimal('0.01'),ROUND_HALF_UP))
            totalmes = float(Decimal(totalmes + mensal).quantize(Decimal('0.01'),ROUND_HALF_UP))

        label = Label(text='Total')
        self.scrl.add_widget(label)
        label = Label(text=str("%.2f" % total))
        self.scrl.add_widget(label)
        label = Label(text='-')
        self.scrl.add_widget(label)
        label = Label(text=str("%.2f" % totalmes))
        self.scrl.add_widget(label)

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


class RelMaqScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total', ' WHERE categoria="Maquinas e Equipamentos"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text = '')
        self.scrl.add_widget(label)
        label = Label(text = 'Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d,str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4*self.height, size_hint=[1,1])
                    else:
                        label = Label(text="%.2f" % float(Decimal(d).quantize(Decimal('0.01'), ROUND_HALF_UP)), font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria="Maquinas e Equipamentos"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


class RelMovScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Moveis e Utensilios"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d, str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4 * self.height, size_hint=[1, 1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria="Moveis e Utensilios"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


class RelPredScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Imoveis Predios"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d, str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4 * self.height, size_hint=[1, 1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo, 'total', ' WHERE categoria="Imoveis Predios"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


class RelTerrScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Imoveis Terrenos"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d, str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4 * self.height, size_hint=[1, 1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo,'total',' WHERE categoria="Imoveis Terrenos"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


class RelVeicScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Fixos em Veiculos"')

        self.scrl.clear_widgets()
        gc.collect()
        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Valor Total')
        self.scrl.add_widget(label)
        x = 1
        for pessoa in dados:
            label = Label(text=str(x))
            self.scrl.add_widget(label)
            for d in pessoa:

                if isinstance(d, str):
                    label = Label(text=d, font_size=0.4 * self.height, size_hint=[1, 1])
                else:
                    if isinstance(d, int):
                        label = Label(text=str(d), font_size=0.4 * self.height, size_hint=[1, 1])
                    else:
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=self.calculaTotal(InvestimentoFixo,'total',' WHERE categoria="Fixos em Veiculos"')))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return str("%.2f" % val)


#Materia prima
class RelMpScreen(Screen):

    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Materia Prima'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        for prod in dados:
            for mp in prod:
                self.criabotao(mp)
    def criabotao(self, nome):
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.preenche(nome))
        self.scrl.add_widget(bt)

    def preenche(self, nome):
        fin = Financeiro()
        print(nome)
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = nome
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))
        x = 1
        dados = MateriaPrima.relatorio(MateriaPrima, 'descricao, unmedida, precounitario, quant, total', ' WHERE produto = "'+nome+'" ORDER BY descricao')

        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Unidade de Medida')
        self.scrl.add_widget(label)
        label = Label(text='Valor Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Total')
        self.scrl.add_widget(label)

        for prod in dados:
            self.scrl.add_widget(Label(text=str(x)))
            for p in prod:
                if p == prod[3] or p == prod[0] or p == prod[1]:
                    self.scrl.add_widget(Label(text=str(p)))
                else:
                    self.scrl.add_widget(Label(text="%.2f" % float(p)))
            x = x+1

        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text="%.2f" % fin.calculaTotal(MateriaPrima, 'total', ' WHERE produto = "'+nome+'"')))


#Estimativa
class RelEstimativaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Estimativa de Vendas'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = str(mes) + ' Mes'
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))
        x = 1
        dados = Estimativa.relatorio(Estimativa, 'descricao, quant, lucrounitario, lucrototal', ' WHERE mes = "'+str(mes)+'" ORDER BY descricao')

        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Lucro Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Lucro Total')
        self.scrl.add_widget(label)

        for prod in dados:
            print(prod)
            self.scrl.add_widget(Label(text=str(x)))
            for p in prod:
                if p == prod[0] or p == prod[1]:
                    self.scrl.add_widget(Label(text=str(p)))
                else:
                    self.scrl.add_widget(Label(text="%.2f" % p))
                    print(p)
            x = x+1

        self.scrl.add_widget(Label(text=' '))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(int(self.calculaTotal(Estimativa, 'quant', ' WHERE mes = "'+str(mes)+'"')))))
        self.scrl.add_widget(Label(text=' '))
        self.scrl.add_widget(Label(text="%.2f" % self.calculaTotal(Estimativa, 'lucrototal', ' WHERE mes = "' + str(mes) + '"')))



    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Custos Fixos Mensais
class RelCustosFixosScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()

        label = Label(text='DESCRICAO')
        self.scrl.add_widget(label)
        label = Label(text='VALOR')
        self.scrl.add_widget(label)

        label = Label(text='MAO-DE-OBRA COM ENCARGOS(GASTO C/ PESSOAL ADMINISTRATIVO')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'maodeobra')))
        self.scrl.add_widget(label)

        label = Label(text='PRÓ-LABORE COM ENCARGOS(GASTOS C/ DIREÇÃO)')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'prolabore')))
        self.scrl.add_widget(label)

        label = Label(text='MATERIAL DE LIMPEZA')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'limpeza')))
        self.scrl.add_widget(label)

        label = Label(text='HONORÁRIOS DO CONTADOR(SERV. TERC. DE CONTABILIDADE)')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'contador')))
        self.scrl.add_widget(label)

        label = Label(text='MATERIAL DE EXPEDIENTE')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'material')))
        self.scrl.add_widget(label)

        label = Label(text='ÁGUA E LUZ')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'agua')))
        self.scrl.add_widget(label)

        label = Label(text='ALUGUEL')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'aluguel')))
        self.scrl.add_widget(label)

        label = Label(text='MANUTENÇÃO')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'manutencao')))
        self.scrl.add_widget(label)

        label = Label(text='DEPRECIAÇÕES/AMORTIZAÇÕES')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'deprec')))
        self.scrl.add_widget(label)

        label = Label(text='OUTROS(OUTROS SERV. TERC., TELEFONE, VERBA P/ AÇÕES SOCIAIS ETC.)')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'outros')))
        self.scrl.add_widget(label)

        label = Label(text='TOTAL')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(CustosFixos, 'total')))
        self.scrl.add_widget(label)

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Investimentos Iniciais
class RelInvIniScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()



        label = Label(text='INVESTIMENTOS INICIAIS')
        self.scrl.add_widget(label)
        label = Label(text='')
        self.scrl.add_widget(label)

        label = Label(text='INVESTIMENTOS FIXOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'totalfixo')))
        self.scrl.add_widget(label)

        label = Label(text='MOVEIS E UTENSILIOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'movs')))
        self.scrl.add_widget(label)

        label = Label(text='MAQUINAS E EQUIPAMENTOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'maqs')))
        self.scrl.add_widget(label)

        label = Label(text='COMPUTADORES E EQ. DE INFORMATICA')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'comps')))
        self.scrl.add_widget(label)

        label = Label(text='VEICULOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'veic')))
        self.scrl.add_widget(label)

        label = Label(text='IMOVEIS PREDIOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'predios')))
        self.scrl.add_widget(label)

        label = Label(text='IMOVEIS E TERRENOS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'terrenos')))
        self.scrl.add_widget(label)

        label = Label(text='OUTROS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'invoutros')))
        self.scrl.add_widget(label)

        label = Label(text='-------------')
        self.scrl.add_widget(label)
        label = Label(text='-----------')
        self.scrl.add_widget(label)

        label = Label(text='DESPESAS PRE-OPERACIONAIS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'totaldesp')))
        self.scrl.add_widget(label)

        label = Label(text='DESPESAS COM LEGALIZACAO')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'legalizacao')))
        self.scrl.add_widget(label)

        label = Label(text='DESPESAS COM DIVULGACAO')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'divulgacao')))
        self.scrl.add_widget(label)

        label = Label(text='OUTROS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'outros')))
        self.scrl.add_widget(label)

        label = Label(text='-------------')
        self.scrl.add_widget(label)
        label = Label(text='-------------')
        self.scrl.add_widget(label)

        label = Label(text='INVESTIMENTOS DE GIRO')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'totalgiro')))
        self.scrl.add_widget(label)

        label = Label(text='ESTOQUES (MATERIA PRIMA)')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'estoque')))
        self.scrl.add_widget(label)

        label = Label(text='CAIXA (RESERVA DE CAIXA)')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'caixa')))
        self.scrl.add_widget(label)

        label = Label(text='OUTROS')
        self.scrl.add_widget(label)
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'outrosg')))
        self.scrl.add_widget(label)

        self.scrl.add_widget(Label(text="TOTAL"))
        label = Label(text="%.2f" % (self.calculaTotal(InvestimentoInicial, 'total')))
        self.scrl.add_widget(label)

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Estoque
class RelEstoqueScreen(Screen):
    @mainthread
    def on_enter(self):
        self.secscreen()

    def secscreen(self):
        self.scrl.clear_widgets()
        gc.collect()

        self.title.text = 'Estoque'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text='Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = str(mes) + ' Mes'
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Voltar(on_release=lambda x: self.secscreen()))
        x = 1
        dados = Estoque.relatorio(Estoque, 'DISTINCT descricao, quant, custounit, custototal',
                                     ' WHERE mes = "' + str(mes) + '"' + 'ORDER BY descricao')

        label = Label(text='')
        self.scrl.add_widget(label)
        label = Label(text='Descricao')
        self.scrl.add_widget(label)
        label = Label(text='Quantidade')
        self.scrl.add_widget(label)
        label = Label(text='Custo Unitario')
        self.scrl.add_widget(label)
        label = Label(text='Custo Total')
        self.scrl.add_widget(label)

        list = []
        prods = []
        quant = 0
        ctt = 0
        for prod in dados:
            print(prod)
            if prod[0] in prods:
                for e in list:
                    if prod[0] == e['descr']:
                        e['quant'] += prod[1]
                        e['custounit'] += prod[2]
                        e['custototal'] += prod[3]

            if prod[0] not in prods:
                prods.append(prod[0])
                list.append({'descr': prod[0], 'quant': prod[1], 'custounit': prod[2], 'custototal': prod[3]})
            print(list)
            #self.scrl.add_widget(Label(text=str(p)))


        for prod in list:
            print(prod)
            self.scrl.add_widget(Label(text=str(x)))
            self.scrl.add_widget(Label(text=str(prod['descr'])))
            self.scrl.add_widget(Label(text=str(prod['quant'])))
            self.scrl.add_widget(Label(text="%.2f" % (prod['custounit'])))
            self.scrl.add_widget(Label(text="%.2f" % (prod['custototal'])))
            quant += prod['quant']
            ctt += prod['custototal']
            x = x + 1


        self.scrl.add_widget(Label(text=' '))
        self.scrl.add_widget(Label(text='TOTAL'))
        #self.scrl.add_widget(Label(text=str(self.calculaTotal(Estoque, 'DISTINCT quant', ' WHERE mes = "' + str(mes) + '"'))))
        self.scrl.add_widget(Label(text=(str(quant))))
        self.scrl.add_widget(Label(text=' '))
        #self.scrl.add_widget(
         #   Label(text=str(self.calculaTotal(Estoque, 'DISTINCT custototal', ' WHERE mes = "' + str(mes) + '"'))))
        self.scrl.add_widget(Label(text="%.2f" % (ctt)))
    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Custo Financeiro Mensal
class RelCustoFinMenScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        fin = Financeiro()
        total = self.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')
        print(total)
        self.scrl.add_widget(Label(text="CUSTO FINANCEIRO MENSAL POR UNIDADE"))
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        self.scrl.add_widget(Label(text=str(custo)))
        print(custo)

        self.scrl.add_widget(Label(text="INVESTIMENTO INICIAL"))
        inv = (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(inv))))
        print(inv)

        self.scrl.add_widget(Label(text="VALOR/MES"))
        valormes = inv*custo
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(valormes))))
        print(valormes)

        for mes in range(1,13):
            self.scrl.add_widget(Label(text=str(mes) + ' MES'))
            if(self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0):
                val = fin.dec(valormes)/self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"')
            else:
                val = 'Erro'
            print(val)
            self.scrl.add_widget(Label(text=str(val)))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Tributos
class RelTribScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        list = ['simples', 'icms', 'pis', 'cofins', 'ipi', 'iss', 'irpj', 'total']

        label = Label(text='TRIBUTO')
        self.scrl.add_widget(label)
        label = Label(text='ALIQUOTA')
        self.scrl.add_widget(label)
        label = Label(text='INDICE')
        self.scrl.add_widget(label)

        total = 0
        ind = 0
        for t in list:

            label = Label(text=t.upper())
            self.scrl.add_widget(label)

            ali = self.preenche(Tributos, t)

            if t != 'total':
                total = total + ali
                ind = ind + (ali/100)

            label = Label(text=str(ali))
            self.scrl.add_widget(label)

            label = Label(text=str(float(Decimal(ali*0.01).quantize(Decimal('0.0001'), ROUND_HALF_UP))))
            self.scrl.add_widget(label)

    def preenche(self, table=None, col=None, cond=None):

        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Custo com Vendas
class RelCustoVendasScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()

        label = Label(text='DESCRICAO')
        self.scrl.add_widget(label)
        label = Label(text='%')
        self.scrl.add_widget(label)
        label = Label(text='INDICE')
        self.scrl.add_widget(label)



        for t in self.listastr(CustoVendas, 'descricao'):
            label = Label(text=t.upper())
            self.scrl.add_widget(label)

            porc = self.preenche(CustoVendas, 'porcentagem', ' WHERE descricao = "'+ t + '"')

            label = Label(text=str(porc))
            self.scrl.add_widget(label)

            label = Label(text=str(porc / 100))
            self.scrl.add_widget(label)

        label = Label(text='TOTAL')
        self.scrl.add_widget(label)
        label = Label(text=str(self.preenche(CustoVendas, 'porcentagem')))
        self.scrl.add_widget(label)
        label = Label(text=str(float(Decimal(self.preenche(CustoVendas, 'porcentagem')/100).quantize(Decimal('0.0001'), ROUND_HALF_UP))))
        self.scrl.add_widget(label)

    def listastr(self, table=None, col=None, cond=None):

        list = table.relatorio(table, col, cond)
        val = []
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "").replace("'","")
                val.append(t)
        return val

    def preenche(self, table=None, col=None, cond=None):

        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Rateio custos fixos
class RelRateioFixoScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        fin = Financeiro()
        total = self.calculaTotal(CustosFixos, 'total')
        dados = RateioFixos.relatorio(RateioFixos, 'produto, porc', ' ORDER BY produto')
        totalt = 0
        totalporc = 0

        self.scrl.add_widget(Label(text="PRODUTO"))
        self.scrl.add_widget(Label(text="% DE RATEIO"))
        self.scrl.add_widget(Label(text="C.FIXO P/ LOTE P/ PROD"))

        for rateio in dados:
            self.scrl.add_widget(Label(text=rateio[0]))
            self.scrl.add_widget(Label(text=str(fin.dec(rateio[1]))))
            totalporc = totalporc + rateio[1]
            totalt = totalt + total*(rateio[1]/100)
            self.scrl.add_widget(Label(text="%.2f" % ((fin.dec(total*rateio[1])/100))))
            print(rateio[0])
        if totalporc == 100:
            pass
        else:
            #exception
            pass

        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=str(totalporc)))
        self.scrl.add_widget(Label(text="%.2f" % (totalt)))



    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Ponto de Equilibrio
class RelPontoEquilibrioScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Ponto de Equilibrio'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioBt())
        #dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        # for prod in dados:
        #
        for mes in range(1,13):
            self.BtMes(mes)


    def BtMes(self, mes):
        bt = Button(text=str(mes) + ' mes')
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def returnMes(self, mes):
        return mes

    def preenche(self, mes):
        fin = Financeiro()
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = "Ponto EQ mes" + str(mes)
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

        total = fin.calculaTotal(CustosFixos, 'total')
        dados = RateioFixos.relatorio(RateioFixos, 'produto, porc')
        totalt = 0
        totalporc = 0
        totalun = 0
        self.scrl.add_widget(Label(text="RATEIO C. FIX"))
        self.scrl.add_widget(Label(text="P. VENDA"))
        self.scrl.add_widget(Label(text="C. VAR."))
        self.scrl.add_widget(Label(text="Nº UNIDADES"))

        prods = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        i = 0
        for rateio in dados:
            totalporc = totalporc + rateio[1]
            totalt = totalt + total*(rateio[1]/100)
            cfixo = (total*rateio[1])/100
            self.scrl.add_widget(Label(text="%.2f" %(cfixo)))
            pv = fin.calculaPV(prods[i][0],mes, 'Preco')
            self.scrl.add_widget(Label(text="%.2f" % (pv)))
            ct = fin.calculaPV(prods[i][0], mes, 'CTotal')
            self.scrl.add_widget(Label(text="%.2f" % (ct)))
            un = cfixo / (pv - ct)
            self.scrl.add_widget(Label(text="%.2f" % (un)))
            totalun += un
            print(str(prods[i][0]) + ' -> ' + str(mes))
            i+=1


        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=str(totalun)))

#Rateio custos operacionais
class RelRateioOpScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()

        total = self.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')
        dados = RateioOp.relatorio(RateioOp, 'produto, porc', ' ORDER BY produto')
        totalt = 0
        totalporc = 0

        self.scrl.add_widget(Label(text="PRODUTO"))
        self.scrl.add_widget(Label(text="% DE RATEIO"))
        self.scrl.add_widget(Label(text="C.FIXO P/ LOTE P/ PROD"))

        for rateio in dados:
            self.scrl.add_widget(Label(text=rateio[0]))
            self.scrl.add_widget(Label(text=str(rateio[1])))
            totalporc = totalporc + rateio[1]
            totalt = totalt + total*(rateio[1]/100)
            self.scrl.add_widget(Label(text="%.2f" % ((total*rateio[1])/100)))

        if totalporc == 100:
            pass
        else:
            #exception
            pass

        self.scrl.add_widget(Label(text="TOTAL"))
        self.scrl.add_widget(Label(text=str(totalporc)))
        self.scrl.add_widget(Label(text="%.2f" % (totalt)))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Preço de venda
class RelPrecoVendaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de Venda'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        for prod in dados:
            for mp in prod:
                self.BtMes(mp)


    def BtMes(self, nome):
        self.title.text = 'Preco de Venda'
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.tryn(nome))
        self.scrl.add_widget(bt)

    def returnMes(self, mes):
        return mes

    def tryn(self, nome):
        self.scrl.clear_widgets()
        gc.collect()
        for mes in range(1,13):
            self.fim(nome,mes)

    def fim(self, nome, mes):
        bt = Button(text=str(mes) + ' mes')
        bt.bind(on_release=lambda x: self.preenche(nome, mes))
        self.scrl.add_widget(bt)

    def preenche(self, nome, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = nome
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))
        x = 1
        fin = Financeiro()
        #Calculos

        mat = self.calculaTotal(MateriaPrima, 'total', ' WHERE produto = "' + nome + '"')

        total = self.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')
        rateio = self.calculaTotal(RateioOp, 'porc', ' WHERE produto = "'+nome+'"')
        op = total * (rateio/100)
        quant = self.calculaTotal(Estimativa, 'quant', ' WHERE descricao = "' + nome + '" AND mes = ' + str(mes))
        if quant != 0:
            cprod = op / quant
        else:
            cprod = 0
        total = self.calculaTotal(CustosFixos, 'total')
        rateio = self.calculaTotal(RateioFixos, 'porc', ' WHERE produto = "' + nome + '"')
        op = total * (rateio / 100)
        quant = self.calculaTotal(Estimativa, 'quant', ' WHERE descricao = "' + nome + '"AND mes = ' + str(mes))
        if quant != 0:
            cfixo = op / quant
        else:
            cfixo = 0
        outros = self.calculaTotal(PrecoVenda, 'outros', ' WHERE mes =' + str(mes) + ' AND produto = "' + nome + '"')

        cip = fin.dec(mat) + fin.dec(cprod) + fin.dec(outros)

        if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
            cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
                  Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"')
        else:
            cfgiro = 0


        lucro = self.calculaTotal(Estimativa, 'lucrounitario', ' WHERE descricao = "' + nome + '" AND mes = ' + str(mes))

        trib = self.calculaTotal(Tributos, 'total') * 0.01
        cvenda = self.calculaTotal(CustoVendas, 'porcentagem') * 0.01
        preco = (fin.dec(cip) + fin.dec(cfixo) + fin.dec(lucro) + fin.dec(cfgiro)) * (1/(1-(trib + fin.dec(cvenda))))

        ctrib = preco * trib
        cdirvendas = preco * cvenda

        ctotal = fin.dec(cip) + fin.dec(ctrib) + fin.dec(cdirvendas) + fin.dec(cfgiro)
        print(self.calculaTotal(CustoFinanceiroMensal, 'custo'))
        print((fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')))
        print(self.calculaTotal(
                  Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"'))
        #Coloca nas widget

        label = Label(text='CUSTO C/ MATERIA PRIMA (MAT. DIRETOS)')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(mat))))

        label = Label(text='CUSTO DE PRODUCAO (OPERACIONAL)')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(cprod))))

        label = Label(text='OUTROS CUSTOS PRODUCAO (TERCEIROS)')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(outros))))

        label = Label(text='CUSTO INDEPENDENTE DO PRECO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(cip))))

        label = Label(text='CUSTO TRIBUTARIO DIRETO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(ctrib))))

        label = Label(text='CUSTO FINANCEIRO DO GIRO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(cfgiro))))

        label = Label(text='CUSTO DIRETO COM VENDAS')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(cdirvendas))))

        label = Label(text='CUSTO TOTAL')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(ctotal))))

        label = Label(text='MARGEM DE CONTRIBUICAO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text=''))

        label = Label(text='CUSTO FIXO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(cfixo))))

        label = Label(text='LUCRO')
        self.scrl.add_widget(label)
        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(lucro))))


        label = Label(text='PRECO DE VENDA')
        self.scrl.add_widget(label)

        self.scrl.add_widget(Label(text="%.2f" % (fin.dec(preco))))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


#Alterar
class AlterarScreen(Screen):
    pass


class AltPessoaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Categoria do cadastro de pessoa:'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(MenuAltBt())
        categoria = ['Producao', 'Administrativo', 'Direcao']
        for cg in categoria:
            self.scrl.add_widget(Label(text=""))
            self.scrl.add_widget(Label(text=""))
            self.criabotao(cg)
            self.scrl.add_widget(Label(text=""))
            self.scrl.add_widget(Label(text=""))

    def criabotao(self, cat):
        bt = Button(text='Pessoal de ' + cat)
        bt.bind(on_release=lambda x: self.preenche(cat))
        self.scrl.add_widget(bt)

    def preenche(self, cat):
        print(cat)
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Alterar pessoal de ' + cat
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.on_enter()))
        dados = Pessoa.relatorio(Pessoa, None, ' WHERE categoria = "' + cat + '"')

        self.scrl.add_widget(Label(text="CARGO"))
        self.scrl.add_widget(Label(text="QUANTIDADE"))
        self.scrl.add_widget(Label(text="SALARIO"))
        self.scrl.add_widget(Label(text="ALTERAR"))
        self.scrl.add_widget(Label(text="DELETAR"))

        for row in dados:
            self.scrl.add_widget(Label(text=str(row[1])))
            self.scrl.add_widget(Label(text=str(row[2])))
            self.scrl.add_widget(Label(text=str(row[3])))
            self.scrl.add_widget(Button(text="A", on_release=lambda x: self.alterar(row, cat)))
            self.scrl.add_widget(Button(text="X", on_release=lambda x: self.deletar(row, cat)))

    def alterar(self, row, cat):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Alterar pessoal de ' + cat
        self.back.clear_widgets()


        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text='Descricao'))
        tx1 = TextInput(text=str(row[1]))
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Quantidade"))
        tx2 = TextInput(text=str(row[2]))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Salario"))
        tx3 = TextInput(text=str(row[3]))
        self.scrl.add_widget(tx3)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.back.add_widget(Button(text="Atualizar", on_release=lambda x: (Pessoa(tx1.text, float(tx2.text), float(tx3.text), cat), self.deletar(row, cat))))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.preenche(cat)))

    def deletar(self, row, cat):
        Banco.delete(Banco, 'pessoa', None, ' WHERE id = '+ str(row[0]))
        self.preenche(cat)


class AltEstimativaScreen(Screen):
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Estimativa de Vendas'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(MenuAltBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Estimativa de vendas do mes ' + str(mes)
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.on_enter()))
        dados = Estimativa.relatorio(Estimativa, None, ' WHERE mes = "' + str(mes) + '" ORDER BY descricao')

        self.scrl.add_widget(Label(text="PRODUTO"))
        self.scrl.add_widget(Label(text="QUANTIDADE"))
        self.scrl.add_widget(Label(text="LUCRO UNITARIO"))
        self.scrl.add_widget(Label(text="ALTERAR - DELETAR"))

        for row in dados:
            self.scrl.add_widget(Label(text=str(row[0])))
            self.scrl.add_widget(Label(text=str(row[1])))
            self.scrl.add_widget(Label(text=str(row[2])))

            self.scrl.add_widget(self.grid(row, mes))

    def grid(self, row, cat):
        gd = GridLayout(cols=2)
        gd.add_widget(Button(text="A", on_release=lambda x: self.alterar(row, cat)))
        gd.add_widget(Button(text="X", on_release=lambda x: self.deletar(row, cat)))
        return gd

    def alterar(self, row, cat):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Alterar estimativa do mes ' + str(cat)
        self.back.clear_widgets()


        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text='Produto'))
        self.scrl.add_widget(Label(text=row[0]))
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Quantidade"))
        tx2 = TextInput(text=str(row[1]))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Lucro Unitario"))
        tx3 = TextInput(text=str(row[2]))
        self.scrl.add_widget(tx3)
        self.scrl.add_widget(Label(text=""))

        self.back.add_widget(Button(text="Atualizar", on_release=lambda x: (Estimativa(row[0], int(tx2.text), float(tx3.text), cat), Estoque(row[0], cat))))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.preenche(cat)))

    def deletar(self, row, cat):
        Banco.delete(Banco, 'estimativa', None, ' WHERE descricao = "'+ str(row[0]) + '" AND quant = ' + str(row[1]) + " AND lucrounitario = " + str(row[2]))
        Banco.delete(Banco, 'estoque', None, ' WHERE descricao = "' + str(row[0]) + '" AND mes = ' + str(cat))
        self.preenche(cat)


class AltInvFixoScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Categoria do cadastro de investimento:'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(MenuAltBt())
        categoria = ['Moveis e Utensilios', 'Maquinas e Equipamentos', 'Computadores/Equipamentos de Informatica', 'Fixos em Veiculos', 'Imoveis Predios', 'Imoveis Terrenos']
        a = 1
        for cg in categoria:
            if a == 1:
                self.scrl.add_widget(Label(text=""))
                a = 0
                self.criabotao(cg)
            else:
                self.criabotao(cg)
                self.scrl.add_widget(Label(text=""))
                a = 1

    def criabotao(self, cat):
        bt = Button(text='Investimento Fixo de ' + cat)
        bt.bind(on_release=lambda x: self.preenche(cat))
        self.scrl.add_widget(bt)


    def preenche(self, cat):
        print(cat)
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Investimento Fixo de ' + cat
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.on_enter()))
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, None, ' WHERE categoria = "' + cat + '"')
        self.scrl.add_widget(Label(text="DESCRICAO"))
        self.scrl.add_widget(Label(text="QUANTIDADE"))
        self.scrl.add_widget(Label(text="VALOR"))
        self.scrl.add_widget(Label(text="ALTERAR - DELETAR"))

        for row in dados:
            self.scrl.add_widget(Label(text=str(row[1])))
            self.scrl.add_widget(Label(text=str(row[2])))
            self.scrl.add_widget(Label(text=str(row[3])))

            self.scrl.add_widget(self.grid(row,cat))

    def grid(self, row, cat):
        gd = GridLayout(cols=2)
        gd.add_widget(Button(text="A", on_release=lambda x: self.alterar(row, cat)))
        gd.add_widget(Button(text="X", on_release=lambda x: self.deletar(row, cat)))
        return gd

    def alterar(self, row, cat):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Alterar pessoal de ' + cat
        self.back.clear_widgets()

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text='Descricao'))
        tx1 = TextInput(text=str(row[1]))
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Quantidade"))
        tx2 = TextInput(text=str(row[2]))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="Salario"))
        tx3 = TextInput(text=str(row[3]))
        self.scrl.add_widget(tx3)
        self.scrl.add_widget(Label(text=""))

        self.back.add_widget(Button(text="Atualizar", on_release=lambda x: (
        InvestimentoFixo(tx1.text, float(tx2.text), float(tx3.text), cat), self.deletar(row, cat))))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.preenche(cat)))


    def deletar(self, row, cat):
        Banco.delete(Banco, 'investimentofixo', None, ' WHERE id = ' + str(row[0]))
        self.preenche(cat)


class AltMatPrimaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Materia Prima'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(MenuAltBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        for prod in dados:
            for mp in prod:
                self.criabotao(mp)

    def criabotao(self, nome):
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.preenche(nome))
        self.scrl.add_widget(bt)

    def preenche(self, nome):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Materias primas do produto ' + str(nome)
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.on_enter()))
        dados = MateriaPrima.relatorio(MateriaPrima, None, ' WHERE produto = "' + str(nome) + '"')

        self.scrl.add_widget(Label(text="DESCRICAO"))
        self.scrl.add_widget(Label(text="UNIDADE DE MEDIDA"))
        self.scrl.add_widget(Label(text="PRECO UNITARIO"))
        self.scrl.add_widget(Label(text="QUANTIDADE"))
        self.scrl.add_widget(Label(text="ALTERAR - DELETAR"))

        for row in dados:
            self.scrl.add_widget(Label(text=str(row[2])))
            self.scrl.add_widget(Label(text=str(row[3])))
            self.scrl.add_widget(Label(text=str(row[4])))
            self.scrl.add_widget(Label(text=str(row[5])))
            self.scrl.add_widget(self.grid(row, nome))

    def grid(self, row, cat):
        gd = GridLayout(cols=2)
        gd.add_widget(Button(text="A", on_release=lambda x: self.alterar(row, cat)))
        gd.add_widget(Button(text="X", on_release=lambda x: self.deletar(row, cat)))
        return gd

    def alterar(self, row, cat):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Alterar materia prima do produto ' + str(cat)
        self.back.clear_widgets()


        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text='DESCRICAO'))
        tx1 = TextInput(text=str(row[2]))
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="UN. MEDIDA"))
        tx2 = TextInput(text=str(row[3]))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="PRECO UNITARIO"))
        tx3 = TextInput(text=str(row[4]))
        self.scrl.add_widget(tx3)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))


        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text="QUANTIDADE"))
        tx4 = TextInput(text=str(row[5]))
        self.scrl.add_widget(tx4)
        self.scrl.add_widget(Label(text=""))
        self.scrl.add_widget(Label(text=""))

        self.back.add_widget(Button(text="Atualizar", on_release=lambda x: (self.parted(row, cat, tx1.text, tx2.text, tx3.text, tx4.text))))
        self.back.add_widget(Button(text='Voltar', on_release=lambda x: self.preenche(cat)))

    def parted(self,row, cat, p1, p2, p3, p4):
        self.deletar(row, cat)
        MateriaPrima(cat, p1, p2, float(p3), float(p4))
        self.preenche(cat)

    def deletar(self, row, cat):
        Banco.delete(Banco, 'materiaprima', None, ' WHERE produto = "'+ cat + '" AND descricao = "' + str(row[2]) + '" AND unmedida = "' + str(row[3]) + '" AND precounitario = ' + str(row[4]) + " AND quant = " + str(row[5]))
        self.preenche(cat)


class AltPrecoVendaScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de Venda'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(MenuAltBt())
        dados = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        print(dados)
        for prod in dados:
            for mp in prod:
                self.BtMes(mp)

    def BtMes(self, nome):
        self.title.text = 'Preco de Venda'
        bt = Button(text=nome)
        bt.bind(on_release=lambda x: self.tryn(nome))
        self.scrl.add_widget(bt)

    def returnMes(self, mes):
        return mes

    def tryn(self, nome):
        self.scrl.clear_widgets()
        gc.collect()
        for mes in range(1, 13):
            self.fim(nome, mes)

    def fim(self, nome, mes):
        bt = Button(text=str(mes) + ' mes')
        bt.bind(on_release=lambda x: self.preenche(nome, mes))
        self.scrl.add_widget(bt)
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def preenche(self, nome, mes):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de Venda'
        self.back.clear_widgets()
        fin = Financeiro()

        self.scrl.add_widget(Label(text='Outros custos'))
        tx1 = TextInput(text=str(fin.calculaTotal(PrecoVenda, 'outros', ' WHERE produto = "'+ nome + '" AND mes =' + str(mes))))
        self.scrl.add_widget(tx1)
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Mes'))
        tx2 = Spinner(text=str(mes),values=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'))
        self.scrl.add_widget(tx2)
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Button(text='Deletar valores', on_release=lambda x: self.deletar(nome, tx2.text, tx1.text)))



        self.back.add_widget(Button(text='Alterar', on_release=lambda x: (self.alterar(nome, tx2.text, tx1.text))))
        self.back.add_widget(Voltar(on_release=lambda x: self.tryn(nome)))

    def alterar(self, nome, mes, val):
        self.deletar(nome,mes,val)
        PrecoVenda(nome, val, mes)
        self.tryn(nome)

    def deletar(self, nome, mes, val):
        Banco.delete(Banco, 'precovenda', None, ' WHERE produto = "' + nome + '" AND mes =' + str(mes))
        self.preenche(nome, mes)

    def grid(self, row, cat):
        gd = GridLayout(cols=2)
        gd.add_widget(Button(text="A", on_release=lambda x: self.alterar(row, cat)))
        gd.add_widget(Button(text="X", on_release=lambda x: self.deletar(row, cat)))
        return gd

#Programação Financeira
class RelPvUnMesScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de venda unitario mensal'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        fin = Financeiro()
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = 'Preco de venda unitario mensal'
        self.scrl.add_widget(Label(text='PRODUTO'))
        self.scrl.add_widget(Label(text='VALOR'))
        produtos = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')

        for prod in produtos:
            self.scrl.add_widget(Label(text=prod[0]))
            self.scrl.add_widget(Label(text="%.2f" % (fin.calculaPV(prod[0], mes, 'Preco'))))

        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))


class RelProjecaoVendasScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Preco de venda unitario mensal'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = 'Projecao de vendas'
        self.scrl.add_widget(Label(text='PRODUTO'))
        self.scrl.add_widget(Label(text='VALOR'))
        produtos = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        total = 0
        for prod in produtos:
            self.scrl.add_widget(Label(text=prod[0]))
            est = self.calculaTotal(Estimativa, 'DISTINCT quant',
                                 ' WHERE mes = ' + str(mes) + ' AND descricao = "' + prod[0] + '"')
            self.scrl.add_widget(Label(text=str(est)))
            total += est

        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(total)))
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


class RelFaturamentoScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Faturamento bruto mensal'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)
        self.scrl.add_widget(Button(text='Total Anual', on_release=lambda x: self.preenche('total')))
    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        fin = Financeiro()
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = 'Faturamento bruto mensal'
        self.scrl.add_widget(Label(text='PRODUTO'))
        self.scrl.add_widget(Label(text='VALOR'))
        produtos = MateriaPrima.relatorio(MateriaPrima, 'DISTINCT produto')
        total = 0
        if mes == 'total':
            val = 0

            for prod in produtos:
                for mon in range(1, 13):
                    est = fin.calculaTotal(Estimativa, 'DISTINCT quant',
                                           ' WHERE mes = ' + str(mon) + ' AND descricao = "' + prod[0] + '"')
                    pv = fin.calculaPV(prod[0], mon, 'Preco')

                    val += est * pv
                total += val
                self.scrl.add_widget(Label(text=prod[0]))
                self.scrl.add_widget(Label(text="%.2f" % (val)))
                val = 0
        else:
            for prod in produtos:
                est = fin.calculaTotal(Estimativa, 'DISTINCT quant',
                                       ' WHERE mes = ' + str(mes) + ' AND descricao = "' + prod[0] + '"')
                pv = fin.calculaPV(prod[0], mes, 'Preco')
                val = est * pv
                total += val
                self.scrl.add_widget(Label(text=prod[0]))
                self.scrl.add_widget(Label(text="%.2f" % (val)))


        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text="%.2f" % (total)))

        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))


class RelCTotalScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Planilha de custos totais'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text = 'Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = 'Preco de venda unitario mensal'
        self.scrl.add_widget(Label(text='DESCRICAO'))
        self.scrl.add_widget(Label(text='MES '+ str(mes)))
        self.desenhaTela(mes)
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def desenhaTela(self, mes):
        fin = Financeiro()
        self.scrl.add_widget(Label(text='CUSTOS C/ PESSOAL ADMINISTRATIVO'))
        adm = fin.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Administrativo"')
        self.scrl.add_widget(Label(text="%.2f" % (adm)))

        self.scrl.add_widget(Label(text='PRÓ-LABORE COM ENCARGOS SOCIAIS'))
        dir = fin.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Diretor"')
        self.scrl.add_widget(Label(text="%.2f" % (dir)))

        self.scrl.add_widget(Label(text='MATERIAL DE LIMPEZA'))
        limpeza = fin.calculaTotal(CustosFixos, 'limpeza')
        self.scrl.add_widget(Label(text="%.2f" % (limpeza)))

        self.scrl.add_widget(Label(text='HONORÁRIOS CONTÁBEIS/OUTROS'))
        contador = fin.calculaTotal(CustosFixos, 'contador')
        self.scrl.add_widget(Label(text="%.2f" % (contador)))

        self.scrl.add_widget(Label(text='MATERIAL DE EXPEDIENTE'))
        material = fin.calculaTotal(CustosFixos, 'material')
        self.scrl.add_widget(Label(text="%.2f" % (material)))

        self.scrl.add_widget(Label(text='ÁGUA E LUZ'))
        agua = fin.calculaTotal(CustosFixos, 'agua')
        self.scrl.add_widget(Label(text="%.2f" % (agua)))

        self.scrl.add_widget(Label(text='ALUGUEL'))
        aluguel = fin.calculaTotal(CustosFixos, 'aluguel')
        self.scrl.add_widget(Label(text="%.2f" % (aluguel)))

        self.scrl.add_widget(Label(text='MANUTENÇÃO'))
        manutencao = fin.calculaTotal(CustosFixos, 'manutencao')
        self.scrl.add_widget(Label(text="%.2f" % (manutencao)))

        self.scrl.add_widget(Label(text='DEPRECIAÇÃO/AMORTIZAÇÃO'))
        deprec = fin.calculaTotal(CustosFixos, 'deprec')
        self.scrl.add_widget(Label(text="%.2f" % (deprec)))

        self.scrl.add_widget(Label(text='OUTROS'))
        outros = fin.calculaTotal(CustosFixos, 'outros')
        self.scrl.add_widget(Label(text="%.2f" % (outros)))

        self.scrl.add_widget(Label(text='TOTAL DOS CUSTOS FIXOS'))
        total = fin.calculaTotal(CustosFixos, 'total')
        self.scrl.add_widget(Label(text="%.2f" % (total)))

        self.scrl.add_widget(Label(text='MÃO-DE-OBRA VARIÁVEL C/ ENCARGOS'))
        pd = fin.calculaTotal(Pessoa, 'total', ' WHERE categoria = "Producao"')
        self.scrl.add_widget(Label(text="%.2f" % (pd)))

        self.scrl.add_widget(Label(text='IMPOSTOS E CONTRIBUIÇÕES'))
        trib = fin.calculaTotal(Tributos, 'total')
        ct = fin.calculaFaturamento(mes)
        imp = ct * (trib/100)
        self.scrl.add_widget(Label(text="%.2f" % (imp)))

        self.scrl.add_widget(Label(text='CUSTO COM VENDAS'))
        cv = fin.calculaTotal(CustoVendas, 'porcentagem')
        cvendas = ct * (cv/100)
        self.scrl.add_widget(Label(text="%.2f" % (cvendas)))

        self.scrl.add_widget(Label(text='MATÉRIA PRIMA'))
        etq = fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = '+ str(mes))
        self.scrl.add_widget(Label(text="%.2f" % (etq)))

        self.scrl.add_widget(Label(text='FRETE'))
        frete = fin.calculaTotal(Frete, 'frete', ' WHERE mes = ' + str(mes))
        self.scrl.add_widget(Label(text="%.2f" % (frete)))

        self.scrl.add_widget(Label(text='TERCEIRIZAÇÃO'))
        pj = Estimativa.relatorio(Estimativa, 'DISTINCT quant',
                                 ' WHERE mes = ' + str(mes))
        opv = PrecoVenda.relatorio(PrecoVenda, 'outros', ' WHERE mes = ' + str(mes))
        ter = 0
        for outros in opv:
            for proj in pj:
                ter += proj[0] * outros[0]
        self.scrl.add_widget(Label(text="%.2f" % (ter)))

        self.scrl.add_widget(Label(text='OUTROS (CUSTO FINANCEIRO, AMORT. etc.)'))
        inv = (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))
        custo = fin.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo
        self.scrl.add_widget(Label(text="%.2f" % (amort)))

        self.scrl.add_widget(Label(text='TOTAL DOS CUSTOS VARIÁVEIS'))
        cvar = pd + imp + cvendas + etq + frete + ter + amort
        self.scrl.add_widget(Label(text="%.2f" % (cvar)))

        self.scrl.add_widget(Label(text='CUSTOS TOTAIS'))
        ctotal = total + cvar
        self.scrl.add_widget(Label(text="%.2f" % (ctotal)))


class RelDemonstrativoScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Demonstrativo de resultados'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)
        self.scrl.add_widget(Button(text='TOTAL ANUAL', on_release= lambda x: self.preenche(" ")))

    def criabotao(self, mes):
        bt = Button(text='Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()

        self.title.text = 'Preco de venda unitario mensal'
        self.scrl.add_widget(Label(text='DESCRICAO'))
        self.scrl.add_widget(Label(text='MES ' + str(mes)))
        self.desenhaTela(mes)
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def desenhaTela(self, mes):

        self.scrl.add_widget(Label(text='RECEITA TOTAL'))
        fat = self.calculaFaturamento(mes)
        self.scrl.add_widget(Label(text=str(fat)))

        self.scrl.add_widget(Label(text='CUSTOS VARIAVEIS'))
        cv = self.custosVariaveis(mes)
        self.scrl.add_widget(Label(text=str(cv)))

        self.scrl.add_widget(Label(text='MARGEM DE CONTRIBUICAO'))
        mc = fat - cv
        self.scrl.add_widget(Label(text=str(mc)))

        self.scrl.add_widget(Label(text='CUSTOS FIXOS'))
        cf = self.calculaTotal(CustosFixos, 'total')
        self.scrl.add_widget(Label(text=str(cf)))

        self.scrl.add_widget(Label(text='LUCRO OPERACIONAL'))
        lucro = mc - cf
        self.scrl.add_widget(Label(text=str(lucro)))

        self.scrl.add_widget(Label(text='IMPOSTO DE RENDA / CONTRIB. SOCIAL'))
        ipr = lucro * (self.calculaTotal(Tributos, 'irpj')/100)
        self.scrl.add_widget(Label(text=str(ipr)))

        reserv = self.calculaTotal(CapGiro, 'reservas')
        self.scrl.add_widget(Label(text='RESERVAS % ' + str(reserv)))
        rv = (lucro*reserv)/100
        self.scrl.add_widget(Label(text=str(rv)))

        self.scrl.add_widget(Label(text='LUCRO LIQUIDO'))
        liquido = lucro - ipr - rv
        self.scrl.add_widget(Label(text=str(liquido)))

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
        fin = Financeiro()
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
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
                    Estimativa, 'quant')
            else:
                cfgiro = 0
        else:
            if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
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
        fin = Financeiro()
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


        inv = fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo


        cvar = pd + imp + cvendas + etq + frete + ter + amort

        return cvar


class RelMargemContribScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'INDICE DE MARGEM DE CONTRIBUICAO'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            fat = self.calculaFaturamento(mes)
            mc = self.custosVariaveis(mes) - fat
            if fat != 0:
                idc = mc / fat
            else:
                idc = 0
            self.scrl.add_widget(Label(text="MES 0" + str(mes)))
            self.scrl.add_widget(Label(text=str(idc)))

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
        fin = Financeiro()
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
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
                    Estimativa, 'quant')
            else:
                cfgiro = 0
        else:
            if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
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
        fin = Financeiro()
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


        inv = fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo


        cvar = pd + imp + cvendas + etq + frete + ter + amort

        return cvar


class RelPontoEqFinScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'INDICE DE MARGEM DE CONTRIBUICAO'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            fat = self.calculaFaturamento(mes)
            mc = self.custosVariaveis(mes) - fat
            if fat != 0:
                idc = mc / fat
                peq = self.calculaTotal(CustosFixos, 'total', ' WHERE mes = ' + str(mes)) / idc
            else:
                peq = 0

            self.scrl.add_widget(Label(text="MES 0" + str(mes)))
            self.scrl.add_widget(Label(text=str(peq)))

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
        fin = Financeiro()
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
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
                    Estimativa, 'quant')
            else:
                cfgiro = 0
        else:
            if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
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
        fin = Financeiro()
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


        inv = fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo


        cvar = pd + imp + cvendas + etq + frete + ter + amort

        return cvar


class RelRentScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'LUCRATIVIDADE, RENTABILIDADE E PRAZO DE RETORNO DE INVESTIMENTO'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        if self.calculaFaturamento(" ") * 100 != 0:
            lucro = self.demonstrativo(" ") / (self.calculaFaturamento(" ") * 100)
        else:
            lucro = 0
        if self.calculaTotal(InvestimentoInicial, 'total') * 100 != 0:
            rent = lucro / (self.calculaTotal(InvestimentoInicial, 'total') * 100)
        else:
            rent = 0
        if lucro != 0:
            pri = self.calculaTotal(InvestimentoInicial, 'total') / lucro
        else:
            pri = 0
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Lucratividade'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='LUCRO LIQUIDO / RECEITA TOTAL * 100'))
        self.scrl.add_widget(Label(text=str(lucro)))
        self.scrl.add_widget(Label(text='%'))

        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Rentabilidade'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='LUCRO LIQUIDO / INVESTIMENTO TOTAL * 100'))
        self.scrl.add_widget(Label(text=str(rent)))
        self.scrl.add_widget(Label(text='%'))

        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='Prazo de retorno de investimento'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='INVESTIMENTO TOTAL / LUCRO LIQUIDO'))
        self.scrl.add_widget(Label(text=str(pri)))
        self.scrl.add_widget(Label(text='%'))

    def demonstrativo(self, mes):
        fat = self.calculaFaturamento(mes)
        cv = self.custosVariaveis(mes)
        mc = fat - cv
        cf = self.calculaTotal(CustosFixos, 'total')

        lucro = mc - cf

        ipr = lucro * (self.calculaTotal(Tributos, 'irpj') / 100)

        reserv = self.calculaTotal(CapGiro, 'reservas')
        rv = (lucro * reserv) / 100
        liquido = lucro - ipr - rv

        return liquido
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
        fin = Financeiro()
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
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
                    Estimativa, 'quant')
            else:
                cfgiro = 0
        else:
            if self.calculaTotal(Estimativa, 'quant', ' WHERE mes ="' + str(mes) + '"') != 0:
                cfgiro = (self.calculaTotal(CustoFinanceiroMensal, 'custo') * (fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial'))) / self.calculaTotal(
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
        fin = Financeiro()
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

        inv = fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')
        custo = self.calculaTotal(CustoFinanceiroMensal, 'custo')
        amort = inv * custo

        cvar = pd + imp + cvendas + etq + frete + ter + amort

        return cvar


class RelTirScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'TIR E VPL'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())

        self.scrl.add_widget(Label(text='TMA'))
        self.scrl.add_widget(Label(text=str(self.calculaTotal(CustoFinanceiroMensal, 'custo')) + ' %'))

        self.scrl.add_widget(Label(text='INVESTIMENTOS'))
        self.scrl.add_widget(Label(text='- ' + str(self.calculaTotal(InvestimentoInicial, 'total'))))

        for mes in range(1,13):
            self.scrl.add_widget(Label(text='MES ' + str(mes)))
            fin = Financeiro()
            self.scrl.add_widget(Label(text=str(fin.demonstrativo(mes, 'liquido'))))

        self.scrl.add_widget(Label(text='TIR'))
        self.scrl.add_widget(Label(text=str(self.calculaTir()*100) + ' %'))
        self.scrl.add_widget(Label(text='VPL'))
        self.scrl.add_widget(Label(text='R$: '+ str(self.calculaVpl())))
    def calculaTir(self):
        fin = Financeiro()
        capital = 0 - self.calculaTotal(InvestimentoInicial, 'total')
        tir = 0- 0.0001
        total = 1
        while(total != 0):
            ll = 0
            tir += 0.0001

            for mes in range(1,13):
                ll += fin.demonstrativo(mes, 'liquido')/((1+tir)**mes)

            total = capital + ll

        return tir

    def calculaVpl(self):
        fin = Financeiro()
        capital = 0 - self.calculaTotal(InvestimentoInicial, 'total')
        tma = self.calculaTotal(CustoFinanceiroMensal, 'custo')

        ll = 0

        for mes in range(1, 13):
            ll += fin.demonstrativo(mes, 'liquido') / ((1 + tma) ** mes)

        vpl = capital + ll

        return vpl


    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


class RelFluxoScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'FLUXO DE CAIXA'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioFinBt())
        for mes in range(1, 13):
            self.criabotao(mes)

    def criabotao(self, mes):
        bt = Button(text='Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = 'FLUXO DE CAIXA'
        fin = Financeiro()

        self.scrl.add_widget(Label(text='ATIVIDADES OPERACIONAIS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='(A) EMBOLSOS OPERACIONAIS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='VENDAS'))
        vendas = fin.calculaFaturamento(mes)
        self.scrl.add_widget(Label(text=str(vendas)))

        self.scrl.add_widget(Label(text='(B) DESEMBOLSOS OPERACIONAIS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='CUSTOS FIXOS'))
        cf = fin.calculaTotal(CustosFixos, 'total')
        self.scrl.add_widget(Label(text=str(cf)))

        self.scrl.add_widget(Label(text='CUSTOS VARIAVEIS (+ IRPJ/CSLL)'))
        cv = fin.custosVariaveis(mes)+fin.demonstrativo(mes,'imposto')
        self.scrl.add_widget(Label(text=str(cv)))

        self.scrl.add_widget(Label(text='(C) FLUXO OPERACIONAL LIQUIDO'))
        fol = vendas - cf - cv
        self.scrl.add_widget(Label(text=str(fol)))

        self.scrl.add_widget(Label(text='ATIVIDADES DE FINANCIAMENTOS'))
        self.scrl.add_widget(Label(text=''))

        if mes == 1:
            self.scrl.add_widget(Label(text='(D) EMBOLSOS DE INVESTIMENTOS'))
            self.scrl.add_widget(Label(text='0'))

            self.scrl.add_widget(Label(text='(E) DESEMBOLSOS PARA INVESTIMENTOS'))
            desinv = fin.calculaTotal(InvestimentoInicial, 'total')
            self.scrl.add_widget(Label(text=str(desinv)))

            self.scrl.add_widget(Label(text='(F) FLUXO DE INVESTIMENTO LIQUIDO'))
            invliq = 0 - desinv
            self.scrl.add_widget(Label(text=str(invliq)))

        self.scrl.add_widget(Label(text='ATIVIDADES DE FINANCIAMENTOS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='(G) EMBOLSOS DE FINANCIAMENTOS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='RECURSOS PROPRIOS'))
        recp = desinv
        self.scrl.add_widget(Label(text=str(recp)))

        self.scrl.add_widget(Label(text='(H) DESEMBOLSOS DE FINANCIAMENTOS'))
        self.scrl.add_widget(Label(text=''))

        self.scrl.add_widget(Label(text='(I) FLUXO DE FINANCIAMENTO LIQUIDO'))
        fluxo = recp
        self.scrl.add_widget(Label(text=str(fluxo - 0)))

        self.scrl.add_widget(Label(text='(J) CAIXA LIQUIDO'))
        caixa = fol + invliq + fluxo
        self.scrl.add_widget(Label(text=str(caixa)))

        if mes == 1:
            saldoini = 0
            saldofim = caixa + saldoini
        if mes != 1:
            saldoini = saldofim
            saldofim = caixa + saldoini

        self.scrl.add_widget(Label(text='(K) SALDO INICIAL DAS DISPONIBILIDADES'))
        self.scrl.add_widget(Label(text=str(saldoini)))

        self.scrl.add_widget(Label(text='(L) SALDO FINAL DAS DISPONIBILIDADES'))
        self.scrl.add_widget(Label(text=str(saldofim)))
        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))


class RelRecebimentosScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'RECEBIMENTOS'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        for mes in range(1, 16):
            self.criabotao(mes)
        self.back.add_widget(Button(text='Total', on_release=lambda x: self.total()))

    def criabotao(self, mes):
        bt = Button(text='Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = 'RECEBIMENTOS'
        fin = Financeiro()

        #calculos
        var = 'Recebimentos'
        fat = fin.calculaFaturamento(mes)
        avista = fin.calculaTotal(CapGiro, 'avista', ' WHERE categoria = "' + var + '"')
        tres = fin.calculaTotal(CapGiro, 'tres', ' WHERE categoria = "' + var + '"')
        seis = fin.calculaTotal(CapGiro, 'seis', ' WHERE categoria = "' + var + '"')
        nove = fin.calculaTotal(CapGiro, 'nov', ' WHERE categoria = "' + var + '"')
        total = avista + tres + seis + nove

        valv = fat * (avista/100)
        valt = fin.calculaFaturamento(mes-1) * (tres/100)
        vals = fin.calculaFaturamento(mes-2) * (seis/100)
        valn = fin.calculaFaturamento(mes-3) * (nove/100)
        valtotal = valv + valt + vals + valn


        #Escreve na tela
        self.scrl.add_widget(Label(text='FATURAMENTO MENSAL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=str(fat)))

        self.scrl.add_widget(Label(text='PRAZO'))
        self.scrl.add_widget(Label(text='%'))
        self.scrl.add_widget(Label(text=str(mes) + ' MES'))

        self.scrl.add_widget(Label(text='A VISTA'))
        self.scrl.add_widget(Label(text=str(avista)))
        self.scrl.add_widget(Label(text=str(valv)))

        self.scrl.add_widget(Label(text='30 DIAS'))
        self.scrl.add_widget(Label(text=str(tres)))
        self.scrl.add_widget(Label(text=str(valt)))

        self.scrl.add_widget(Label(text='60 DIAS'))
        self.scrl.add_widget(Label(text=str(seis)))
        self.scrl.add_widget(Label(text=str(vals)))

        self.scrl.add_widget(Label(text='90 DIAS'))
        self.scrl.add_widget(Label(text=str(nove)))
        self.scrl.add_widget(Label(text=str(valn)))

        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(total)))
        self.scrl.add_widget(Label(text=str(valt)))

        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))
    def total(self):
        pass


class RelPagamentosScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Pagamentos'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        for mes in range(1, 16):
            self.criabotao(mes)
        self.back.add_widget(Button(text='Total', on_release=lambda x: self.total()))

    def criabotao(self, mes):
        bt = Button(text='Mes ' + str(mes))
        bt.bind(on_release=lambda x: self.preenche(mes))
        self.scrl.add_widget(bt)

    def preenche(self, mes):
        self.scrl.clear_widgets()
        self.back.clear_widgets()
        gc.collect()
        self.title.text = 'Pagamentos'
        fin = Financeiro()

        var = 'Pagamentos'
        fat = fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes))
        valv = fin.calculaTotal(CapGiro, 'avista', ' WHERE categoria = "' + var + '"') * (fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes)) / 100)
        if mes == 1:
            valt = 0
        else:
            valt = fin.calculaTotal(CapGiro, 'tres', ' WHERE categoria = "' + var + '"') * (fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes - 1))  / 100)
        if mes == 1 or mes == 2:
            vals = 0
        else:
            vals = fin.calculaTotal(CapGiro, 'seis', ' WHERE categoria = "' + var + '"') * (fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes - 2))  / 100)
        if mes == 1 or mes == 2 or mes == 3:
            valn = 0
        else:
            valn = fin.calculaTotal(CapGiro, 'nov', ' WHERE categoria = "' + var + '"') * (fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = ' + str(mes - 3))  / 100)

        avista = fin.calculaTotal(CapGiro, 'avista', ' WHERE categoria = "' + var + '"')
        tres = fin.calculaTotal(CapGiro, 'tres', ' WHERE categoria = "' + var + '"')
        seis = fin.calculaTotal(CapGiro, 'seis', ' WHERE categoria = "' + var + '"')
        nove = fin.calculaTotal(CapGiro, 'nov', ' WHERE categoria = "' + var + '"')
        total = avista + tres + seis + nove
        valtotal = valv + valt + vals + valn

        # Escreve na tela
        self.scrl.add_widget(Label(text='PAGAMENTO MENSAL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=str(fat)))

        self.scrl.add_widget(Label(text='PRAZO'))
        self.scrl.add_widget(Label(text='%'))
        self.scrl.add_widget(Label(text=str(mes) + ' MES'))

        self.scrl.add_widget(Label(text='A VISTA'))
        self.scrl.add_widget(Label(text=str(avista)))
        self.scrl.add_widget(Label(text=str(valv)))

        self.scrl.add_widget(Label(text='30 DIAS'))
        self.scrl.add_widget(Label(text=str(tres)))
        self.scrl.add_widget(Label(text=str(valt)))

        self.scrl.add_widget(Label(text='60 DIAS'))
        self.scrl.add_widget(Label(text=str(seis)))
        self.scrl.add_widget(Label(text=str(vals)))

        self.scrl.add_widget(Label(text='90 DIAS'))
        self.scrl.add_widget(Label(text=str(nove)))
        self.scrl.add_widget(Label(text=str(valn)))

        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(total)))
        self.scrl.add_widget(Label(text=str(valtotal)))

        self.back.add_widget(Voltar(on_release=lambda x: self.on_enter()))

    def total(self):
        pass


class RelMinScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Outros Relatorios'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()
        #calculos
        receber = fin.calculaPagRec(" ", 'Recebimentos')
        pagar = fin.calculaPagRec(" ", 'Pagamentos')
        receita = fin.calculaFaturamento(" ")
        canual = fin.calculaTotal(Estoque, 'custototal')
        if receita != 0:
            pmrv = (receber / receita) * 360
        else:
            pmrv = 0
        if canual != 0:
            pmpc = (pagar / canual) * 360
        else:
            pmpc = 0
        pmre = (fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = 1') + fin.calculaTotal(Estoque, 'custototal', ' WHERE mes = 12') / 2 ) * 360
        #preenche
        self.scrl.add_widget(Label(text='CONTAS A RECEBER APÓS 12º MÊS'))
        self.scrl.add_widget(Label(text=str(receber)))

        self.scrl.add_widget(Label(text='CONTAS A PAGAR APÓS 12º MÊS'))
        self.scrl.add_widget(Label(text=str(pagar)))

        self.scrl.add_widget(Label(text='RECEITA ANUAL'))
        self.scrl.add_widget(Label(text=str(receita)))

        self.scrl.add_widget(Label(text='CUSTO ANUAL COM MATERIAL DIRETO'))
        self.scrl.add_widget(Label(text=str(canual)))

        self.scrl.add_widget(Label(text='PMRV'))
        self.scrl.add_widget(Label(text=str(pmrv) + ' DIAS'))

        self.scrl.add_widget(Label(text='PMPC'))
        self.scrl.add_widget(Label(text=str(pmpc) + ' DIAS'))

        self.scrl.add_widget(Label(text='PMRE'))
        self.scrl.add_widget(Label(text=str(pmre) + ' DIAS'))


class RelCapGiroScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Capital de Giro'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='DESCRICAO'))
        self.scrl.add_widget(Label(text='R$'))
        self.scrl.add_widget(Label(text='ESTOQUE INICIAL'))
        self.scrl.add_widget(Label(text=str(fin.calculaTotal(Estoque, 'custototal')/12)))
        self.scrl.add_widget(Label(text='CAIXA MINIMO'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('total'))))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(fin.capGiro())))


class RelInvPreOpScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Investimentos Pre-Operacionais'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='DESPESAS COM LEGALIZACAO'))
        self.scrl.add_widget(Label(text=str(fin.calculaTotal(InvestimentoInicial, 'legalizacao'))))
        self.scrl.add_widget(Label(text='DIVULGACAO'))
        self.scrl.add_widget(Label(text=str(fin.calculaTotal(InvestimentoInicial, 'divulgacao'))))
        self.scrl.add_widget(Label(text='OUTRAS DESPESAS (OBRAS CIVIS/CURSOS E TREINAMENTOS ETC.'))
        self.scrl.add_widget(Label(text=str(fin.calculaTotal(InvestimentoInicial, 'outros'))))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(fin.calculaInvPreOp())))


class RelCalcScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Calculo da Necessidade de Capital de Giro em Dias'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='RECURSOS DA EMPRESA FORA DE SEU CAIXA'))
        self.scrl.add_widget(Label(text='N DE DIAS'))
        self.scrl.add_widget(Label(text='1. CONTAS A RECEBER-PRAZO MEDIO DE VENDAS'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('rec'))))
        self.scrl.add_widget(Label(text='2. ESTOQUES (NECESSIDADE MEDIA DE ESTOQUES)'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('est'))))
        self.scrl.add_widget(Label(text='Subtotal 1(1+2)'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('sub'))))
        self.scrl.add_widget(Label(text='RECURSOS DE TERCEIROS NO CAIXA DA EMPRESA'))
        self.scrl.add_widget(Label(text='N DE DIAS'))
        self.scrl.add_widget(Label(text='3. FORNECEDORES PRAZO MEDIO DE COMPRAS'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('forn'))))
        self.scrl.add_widget(Label(text='Subtotal 2 (3)'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('sub2'))))
        self.scrl.add_widget(Label(text='NECESSIDADE LIQUIDA DE CAPITAL DE GIRO EM DIAS'))
        self.scrl.add_widget(Label(text=str(fin.necessidadeGiro('liq'))))


class RelCaixaMinScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Caixa Minimo'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='1. CUSTO FIXO MENSAL'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('cf'))))
        self.scrl.add_widget(Label(text='2. CUSTO VARIAVEL MENSAL'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('cv'))))
        self.scrl.add_widget(Label(text='3. CUSTO TOTAL DA EMPRESA'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('ct'))))
        self.scrl.add_widget(Label(text='4. CUSTO TOTAL DIARIO'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('ctd'))))
        self.scrl.add_widget(Label(text='5. NECESSIDADE LIQUIDA DE CAPITAL DE GIRO EM DIAS'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('need'))))
        self.scrl.add_widget(Label(text='TOTAL DE B-CAIXA MINIMO (ITEM 4X5)'))
        self.scrl.add_widget(Label(text=str(fin.caixaMin('total'))))


class RelBalancoIniScreen(Screen):
    @mainthread
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Balanco Inicial'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='1 - ATIVO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='2 - PASSIVO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='11 - CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='21 - CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='111 - DISPONIVEL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='211 - OBRIGACOES COM FORNECEDORES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1111 - CAIXA'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('caixa'))))
        self.scrl.add_widget(Label(text='2111 - FORNECEDORES A PAGAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('fornecedores'))))
        self.scrl.add_widget(Label(text='114 - ESTOQUES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='212 - OBRIGACOES FINANCEIRAS'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1141 - ESTOQUES'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('estoques'))))
        self.scrl.add_widget(Label(text='2121 - EMPRESTIMOS A PAGAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('emprestimos'))))
        self.scrl.add_widget(Label(text='1142 - OUTROS ESTOQUES'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('outrosest'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='115 - DESPESAS DE EXERCICIOS SEGUINTES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1157 - DESPESAS A AMORTIZAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('despesas'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='12 - NAO CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='24 - PATRIMONIO LIQUIDO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='123 - IMOBILIZADO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='241 - CAPITAL SOCIAL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1231 - IMOVEIS TERRENOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('terrenos'))))
        self.scrl.add_widget(Label(text='2411 - CAPITAL SOCIAL'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('capsocial'))))
        self.scrl.add_widget(Label(text='1232 - IMOVEIS PREDIOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('predios'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1234 - VEICULOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('veiculos'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1236 - MOVEIS E UTENSILIOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('moveis'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1238 - COMPUTADORES E EQUIPS. DE INF.'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('computador'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='12310 - MAQUINAS E EQUIPAMENTOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('maquinas'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='TOTAL DO ATIVO'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('totalativo'))))
        self.scrl.add_widget(Label(text='TOTAL DO PASSIVO'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('totalpassivo'))))


class RelBalancoProjScreen(Screen):
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'Balanco Projetado'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        self.scrl.add_widget(Label(text='1 - ATIVO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='2 - PASSIVO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='11 - CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='21 - CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='111 - DISPONIVEL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='211 - OBRIGACOES COM FORNECEDORES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1111 - CAIXA'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('caixa'))))
        self.scrl.add_widget(Label(text='2111 - FORNECEDORES A PAGAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('fornecedores'))))
        self.scrl.add_widget(Label(text='114 - ESTOQUES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='212 - OBRIGACOES FINANCEIRAS'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1141 - ESTOQUES'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('estoques'))))
        self.scrl.add_widget(Label(text='2121 - EMPRESTIMOS A PAGAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('emprestimos'))))
        self.scrl.add_widget(Label(text='1142 - OUTROS ESTOQUES'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('outrosest'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='115 - DESPESAS DE EXERCICIOS SEGUINTES'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1157 - DESPESAS A AMORTIZAR'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('despesas'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1158 - (-)DESPESAS AMORTIZADAS'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('-despesas'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='12 - NAO CIRCULANTE'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='24 - PATRIMONIO LIQUIDO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='123 - IMOBILIZADO'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='241 - CAPITAL SOCIAL'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1231 - IMOVEIS TERRENOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('terrenos'))))
        self.scrl.add_widget(Label(text='2411 - CAPITAL SOCIAL'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('capsocial'))))
        self.scrl.add_widget(Label(text='1232 - IMOVEIS PREDIOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('predios'))))
        self.scrl.add_widget(Label(text='243 - LUCROS OU PREJUIZOS ACUMULADOS'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1233 - (-)DEPR. ACUMULADA DE IMOVEIS'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('-imoveis'))))
        self.scrl.add_widget(Label(text='2431 - LUCRO ACUMULADO'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('lucro'))))
        self.scrl.add_widget(Label(text='1234 - VEICULOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('veiculos'))))
        self.scrl.add_widget(Label(text='244 - RESERVAS'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1235 - (-)DEPR. ACUMULADA DE VEICULOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('-veiculos'))))
        self.scrl.add_widget(Label(text='2441 - RESERVAS'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('reservas'))))
        self.scrl.add_widget(Label(text='1236 - MOVEIS E UTENSILIOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('moveis'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1237 - (-)DEPR. ACUMULADA DE MOV. UTENS.'))
        self.scrl.add_widget(Label(text=str(fin.balancoProj('-moveis'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1238 - COMPUTADORES E EQUIPS. DE INF.'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('computador'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='1237 - (-)DEPR. ACUMULADA DE EQUIPS. INF.'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('-computador'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='12310 - MAQUINAS E EQUIPAMENTOS'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('maquinas'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='12311 - (-)DEPR. ACUMULADA DE MAQS. EQUIP.'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('-computador'))))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='TOTAL DO ATIVO'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('totalativo'))))
        self.scrl.add_widget(Label(text='TOTAL DO PASSIVO'))
        self.scrl.add_widget(Label(text=str(fin.balancoIni('totalpassivo'))))


class RelRecursosScreen(Screen):
    def on_enter(self):
        self.scrl.clear_widgets()
        gc.collect()
        self.title.text = 'ORIGEM E FONTE DOS RECURSOS'
        self.back.clear_widgets()
        self.back.add_widget(Label(text=""))
        self.back.add_widget(RelatorioGiroBt())
        fin = Financeiro()

        forn = fin.balancoIni('fornecedores')/fin.balancoIni('totalpassivo')*100
        emp = fin.balancoIni('emprestimos')/fin.balancoIni('totalpassivo')*100
        cap = 100 - forn - emp

        terc = forn + emp
        prop = fin.balancoIni('capsocial')
        total = terc + prop

        self.scrl.add_widget(Label(text='DESCRICAO'))
        self.scrl.add_widget(Label(text='%'))
        self.scrl.add_widget(Label(text='FORNECEDORES'))
        self.scrl.add_widget(Label(text=str(forn)))
        self.scrl.add_widget(Label(text='EMPRESTIMOS'))
        self.scrl.add_widget(Label(text=str(emp)))
        self.scrl.add_widget(Label(text='CAPITAL SOCIAL'))
        self.scrl.add_widget(Label(text=str(cap)))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text='100'))

        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='FONTE DOS RECURSOS'))
        self.scrl.add_widget(Label(text=''))
        self.scrl.add_widget(Label(text='CAPITAIS DE TERCEIROS'))
        self.scrl.add_widget(Label(text=str(terc)))
        self.scrl.add_widget(Label(text='CAPITAIS PROPRIOS'))
        self.scrl.add_widget(Label(text=str(prop)))
        self.scrl.add_widget(Label(text='TOTAL'))
        self.scrl.add_widget(Label(text=str(total)))

# Functions
class StartButton(Button):
    pass


class ScrollGridCustom(BoxLayout):
    pass


class SendButton(Button):
    pass


class Voltar(Button):
    pass


class RelatorioBt(Button):
    pass


class RelatorioFinBt(Button):
    pass


class RelatorioGiroBt(Button):
    pass


class MenuAltBt(Button):
    pass


class CadastroBt(Button):
    pass


class EnviaBt(Button):
    pass


kv_path = './Interface/kv/'
for kv in listdir(kv_path):
    if kv.find('.kv') is not -1:
        Builder.load_file(kv_path + kv)

kv_path = './Interface/kv/Cadastro/'
for kv in listdir(kv_path):
    if kv.find('.kv') is not -1:
        Builder.load_file(kv_path + kv)

kv_path = './Interface/kv/Relatorios/'
for kv in listdir(kv_path):
    if kv.find('.kv') is not -1:
        Builder.load_file(kv_path + kv)

kv_path = './Interface/kv/Alterar/'
for kv in listdir(kv_path):
    if kv.find('.kv') is not -1:
        Builder.load_file(kv_path + kv)

start = Builder.load_file('./Interface/kv/main.kv')

class Interface(App):

    def build(self):
        self.title = "GIBATABLE"
        return start
