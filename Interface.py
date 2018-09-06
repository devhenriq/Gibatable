from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from os import listdir
from Pessoa import Pessoa
from InvestimentoFixo import InvestimentoFixo
from MateriaPrima import MateriaPrima
from Estimativa import Estimativa
from CustosFixos import CustosFixos
from Tributos import Tributos

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
