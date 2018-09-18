from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from os import listdir
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
from kivy.clock import mainthread
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from functools import partial
import gc


Window.fullscreen = False
Config.set('graphics', 'resizable', False)
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
        m = MateriaPrima(self.nome.text, self.materia.text, self.medida.text, float(self.preco.text), int(self.quant.text))
        m.relatorio()
        self.nome.text = ""
        self.materia.text = ""
        self.medida.text = ""
        self.preco.text = ""
        self.quant.text = ""


class EstimativaScreen(Screen):
    def envia(self):
        e = Estimativa(self.descr.text, int(self.quant.text), float(self.lucro.text), self.mes.text)
        e.relatorio()
        self.descr.text = ""
        self.quant.text = ""
        self.lucro.text = ""
        self.mes.text = "-"
        est = Estoque()
        est.relatorio()


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
        #Clock.schedule_once(self.create_scrollview)

   # def create_scrollview(self):
        for w in self.inputs:
            w[0].canvas.clear()
            w[1].canvas.clear()
            w[2].canvas.clear()

        #scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))


        list = Estimativa.relatorio(Estimativa, 'descricao')

        x = 0
        for e in list:
            lista = []

            label = Label(text=e[0])
            self.scrl.add_widget(label)
            lista.append(label)

            textin = TextInput(font_size=32,multiline=False)
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
            rto = RateioFixos(w)  # adicionar na lista os inputs criado na linha 160 dos text input. (15 linhas abaixo)k
            rto.relatorio()

    @mainthread
    def on_enter(self):
        # Clock.schedule_once(self.create_scrollview)

        # def create_scrollview(self):
        for w in self.inputs:
            w[0].canvas.clear()
            w[1].canvas.clear()
            w[2].canvas.clear()

        # scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))

        list = Estimativa.relatorio(Estimativa, 'descricao')

        x = 0
        for e in list:
            lista = []

            label = Label(text=e[0])
            self.scrl.add_widget(label)
            lista.append(label)

            textin = TextInput(font_size=32, multiline=False)
            self.scrl.add_widget(textin)
            lista.append(textin)

            label2 = Label(text='%')
            self.scrl.add_widget(label2)
            lista.append(label2)

            self.inputs.append(lista)
            x = x + 1


class PrecoVendaScreen(Screen):
    def envia(self):
        pv = PrecoVenda(self.outros.text, self.mes.text)
        pv.relatorio()
        self.outros.text = ""
        self.mes.text = ""

#Relatorio
class RelatorioScreen(Screen):
    pass

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

class RelPessoaOpScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = Pessoa.relatorio(Pessoa, 'cargo, quant, salario, ferias, decimo, fgts, inss, total', ' WHERE categoria="Produtor"')

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


class RelInvFixoScreen(Screen):
    pass

class RelCompScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total', ' WHERE categoria="Computadores/Equipamentos de Informatica"')

        self.scrl.clear_widgets()
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
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1

class RelDeprecScreen(Screen):
    pass

class RelMaqScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total', ' WHERE categoria="Maquinas e Equipamentos"')

        self.scrl.clear_widgets()
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
                        label = Label(text="%.2f" % d, font_size=0.4 * self.height, size_hint=[1, 1])
                self.scrl.add_widget(label)
            x = x + 1

class RelMovScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Moveis e Utensilios"')

        self.scrl.clear_widgets()
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

class RelPredScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Imoveis Predios"')

        self.scrl.clear_widgets()
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

class RelTerrScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Imoveis Terrenos"')

        self.scrl.clear_widgets()
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

class RelVeicScreen(Screen):
    @mainthread
    def on_enter(self):
        dados = InvestimentoFixo.relatorio(InvestimentoFixo, 'descricao, quant, valorunitario, total',
                                           ' WHERE categoria="Fixos em Veiculos"')

        self.scrl.clear_widgets()
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

class AlterarScreen(Screen):
    pass

# Functions
class StartButton(Button):
    pass

class ScrollGridCustom(BoxLayout):
    pass

class SendButton(Button):
    pass

class Voltar(Button):
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

start = Builder.load_file('./Interface/kv/main.kv')

class Interface(App):

    def build(self):
        self.title = "GIBATABLE"
        return start
