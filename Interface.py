from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.config import Config

from os import listdir
kv_path = './Interface/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)

Window.fullscreen = False
Config.set('graphics', 'resizable', 1)
Config.write()

# class LoginScreen(GridLayout):
#
#     def __init__(self, **kwargs):
#         #super(LoginScreen, self).__init__(**kwargs)
#         self.cols = 3
#         self.add_widget(Label(text='Gibatable'))
#         #self.username = TextInput(multiline=False)
#         #self.add_widget(self.username)
#         #self.add_widget(Label(text='password'))
#         #self.password = TextInput(password=True, multiline=False)
#         #self.add_widget(self.password)
#class MenuScreen(FloatLayout):


class StartScreen(FloatLayout):

    #display = ObjectProperty()

    def add_one(self):
        #value = int(self.display.text)
        self.display.text = "EI"

    def subtract_one(self):
        #value = int(self.display.text)
        self.display.text = "HO"

class StartButton(Button):
    pass

class SendButton(Button):
    pass

class Interface(App):

    def build(self):
        self.title = "GIBATABLE"
        return StartScreen()
