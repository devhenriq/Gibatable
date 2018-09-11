from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
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
from kivy.clock import mainthread
from kivy.uix.slider import Slider

Window.fullscreen = False
Config.set('graphics', 'resizable', 1)
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
            #rto = RateioOp(self.inputs) #adicionar na lista os inputs criado na linha 160 dos text input. (15 linhas abaixo)
            #rto.relatorio()
            print()

    @mainthread
    def on_enter(self):
        slider = Slider()
        self.add_widget(slider)
        list = Estimativa.relatorio(Estimativa, 'descricao')

        x = 0
        for e in list:

            label = Label(size_hint=[1, 1], text=e[0], pos_hint={'top': 7 - x, 'right': 2})
            self.add_widget(label)
            textin = TextInput(id='porc'+str(x), size_hint=[1,.45], pos_hint={'top': 6.7 - x, 'right': 4}, multiline=False)
            self.add_widget(textin)
            self.inputs.append('porc'+str(x))
            x = x + 1


class RateioCustosOpScreen(Screen):
    def envia(self):
        pass

    @mainthread
    def on_enter(self):
        slider = Slider()
        self.add_widget(slider)
        list = Estimativa.relatorio(Estimativa, 'descricao')

        x = 0
        for e in list:

            label = Label(size_hint=[1, 1], text=e[0], pos_hint={'top': 7 - x, 'right': 2})
            self.add_widget(label)
            textin = TextInput(size_hint=[1,.45], pos_hint={'top': 6.7 - x, 'right': 4}, multiline=False)
            self.add_widget(textin)
            x = x + 1

class PrecoVendaScreen(Screen):
    def envia(self):
        pass


#Relatorio
class RelatorioScreen(Screen):
    pass


class AlterarScreen(Screen):
    pass

# Functions
class StartButton(Button):
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
