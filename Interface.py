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


class Cadastro(Screen):
    pass

# Cadastro
class PessoaScreen(Screen):
    def envia(self):
        p = Pessoa(self.cargo.text, int(self.quant.text), float(self.salario.text), self.categoria.text)
        p.relatorio()


class Investimento(Screen):
    def envia(self):
        i = InvestimentoFixo(self.descr.text, int(self.quant.text), float(self.vunit.text), self.categoria.text)
        i.relatorio()

class MateriaPrimaScreen(Screen):
    def envia(self):
        m = MateriaPrima(self.nome.text, self.materia.text, self.medida.text, float(self.preco.text), int(self.quant.text))
        m.relatorio()


class EstimativaScreen(Screen):
    def envia(self):
        e = Estimativa(self.descr.text, int(self.quant.text), float(self.lucro.text), int(self.quant.text))
        e.relatorio()


class CustosFixosScreen(Screen):
    def envia(self):
        c = CustosFixos(float(self.limp.text), float(self.cont.text), float(self.mat.text), float(self.agua.text), float(self.aluguel.text), float(self.man.text), float(self.outros.text))
        c.relatorio()

#Relatorio
class Relatorio(Screen):
    pass


class Alterar(Screen):
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
