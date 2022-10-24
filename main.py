from kivy.config import Config

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)

import calculation
import json
import threading
import time
import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore

autosave = True
button_size = [0, .15]

data = JsonStore('data_file.json')
try:
    text = data.get('data')['text']
except KeyError:
    data.put('data')
    text = ''


class Input(TextInput):
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.chekcing_focus = threading.Thread(target=self.check_focus)
        self.chekcing_focus.start()

    def check_focus(self):
        global button_size
        while autosave:
            time.sleep(0.3)
            value = self.focus
            if value:
                app.button.size_hint = [1, 0.6]
            else:
                app.button.size_hint = [1, 0.15]


class MyApp(App):
    def build(self):
        layout = GridLayout(rows=3, cols=1)
        self.text_input = Input(text=text, background_color=[.17, .17, .17, 1], foreground_color=[.9, .9, .9, 1],
                                text_language='ru', font_size=28, padding=[10, 0, 10, 0])
        layout.add_widget(self.text_input)
        self.button = Button(text='Посчитать', on_press=self.click_button, size_hint=button_size)
        layout.add_widget(self.button)
        return layout

    def click_button(self, instance):
        global button_size
        calculation.give_data(self.text_input._get_text())
        content = GridLayout(cols=1, rows=3, padding=[10])
        self.popup = Popup(size_hint=(.7, .6), title='Результат', title_align='center',
                           title_size=20, content=content)
        self.popup.open()
        content.add_widget(Label(text=calculation.label))
        content.add_widget(Label(text=f'Общее: {str(calculation.overall_score)}', font_size=25))
        content.add_widget(Button(text='Закрыть', on_press=self.close_popup, size_hint=[1, 0.6]))

    def close_popup(self, instance):
        self.popup.dismiss()


def autosave():
    while autosave:
        time.sleep(2)
        data['data'] = {'text': app.text_input._get_text()}
    sys.exit()


if __name__ == '__main__':
    app = MyApp()
    saver = threading.Thread(target=autosave)
    saver.start()
    app.run()

try:
    pass
finally:
    autosave = False
