from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.properties import ObjectProperty


from os import listdir
kv_path = './Interface/kv/'
for kv in listdir(kv_path):
    Builder.load_file(kv_path+kv)


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

# class StartScreen():
#
#     def __init__(self, **kwargs):
#         super(StartScreen, self).__init__(**kwargs)
#         self.FloatLayout(size=(1500, 1500))
#         self.add_widget(Label(text='Gibatable'))

class StartScreen(GridLayout):
    display = ObjectProperty()

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
