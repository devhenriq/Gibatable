from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import StringProperty, ListProperty

from os import listdir

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


class Relatorio(Screen):
    pass


class Alterar(Screen):
    pass

# Functions
class StartButton(Button):
    pass


class SendButton(Button):
    pass


kv_path = './Interface/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)
start = Builder.load_file('./Interface/kv/main.kv')

class Interface(App):

    def build(self):
        self.title = "GIBATABLE"
        return start
