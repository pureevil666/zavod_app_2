from kivy.config import Config

Config.set('graphics', 'resizable', 0)
import calculation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label

Window.size = (400, 600)


class MyApp(App):
    def build(self):
        layout = GridLayout(rows=2)
        self.text_input = TextInput(background_color=[.17, .17, .17, 1], foreground_color=[.9, .9, .9, 1])
        layout.add_widget(self.text_input)
        layout.add_widget(Button(text='Посчитать', on_press=self.click_button, size_hint=[1, 0.12]))
        return layout

    def click_button(self, instance):
        calculation.give_data(self.text_input._get_text())
        content = GridLayout(cols=1, rows=3, padding=[10])
        self.popup = Popup(size_hint=(.7, .6), title='Результат', title_align='center',
                           title_size=20, content=content)
        self.popup.open()
        content.add_widget(Label(text=calculation.label))
        content.add_widget(Label(text=f'Общее: {str(calculation.overall_score)}', font_size=20))
        content.add_widget(Button(text='Закрыть', on_press=self.close_popup, size_hint=[1, 0.3]))

    def close_popup(self, instance):
        self.popup.dismiss()


if __name__ == '__main__':
    MyApp().run()
