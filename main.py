from kivy.config import Config

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)

import calculation
import json
import threading
import time
import datetime
import sys
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore

autosave = True
date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
print(date)
data = JsonStore('data_file.json')
month_dict = {'1': 'янв',
              '2': 'фев',
              '3': 'мар',
              '4': 'апр',
              '5': 'май',
              '6': 'июн',
              '7': 'июл',
              '8': 'авг',
              '9': 'сен',
              '10': 'окт',
              '11': 'ноя',
              '12': 'дек',
              }

try:
    text = data.get('data')[date]
except KeyError:
    data.put('data')
    text = ''
    data['data'] = {date: text}


class Input(TextInput):
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.chekcing_focus = threading.Thread(target=self.check_focus)
        self.chekcing_focus.start()

    def check_focus(self):
        while autosave:
            time.sleep(0.3)
            value = self.focus
            if value:
                app.bottom_layout.size_hint = [1, 0.6]
            else:
                app.bottom_layout.size_hint = [1, 0.15]


class MyApp(App):
    def build(self):
        self.day = datetime.datetime.strftime(datetime.datetime.now(), "%d")
        self.month = datetime.datetime.strftime(datetime.datetime.now(), "%m")
        self.year = datetime.datetime.strftime(datetime.datetime.now(), "%Y")
        main_layout = GridLayout(rows=2, cols=1)
        self.text_input = Input(text=text, background_color=[.17, .17, .17, 1], foreground_color=[.9, .9, .9, 1],
                                text_language='ru', font_size=28, padding=[10, 0, 10, 0])
        main_layout.add_widget(self.text_input)

        self.bottom_layout = GridLayout(rows=1, cols=2)
        self.button_count = Button(text='Посчитать', font_size=24, on_press=self.button_count_click)
        self.button_date = Button(text='История', font_size=24, on_press=self.button_date_click)
        self.bottom_layout.add_widget(self.button_count)
        self.bottom_layout.add_widget(self.button_date)

        main_layout.add_widget(self.bottom_layout)
        return main_layout

    def button_count_click(self, instance):
        calculation.give_data(self.text_input._get_text())
        content = GridLayout(cols=1, rows=3, padding=[10])
        self.popup_count = Popup(size_hint=(.7, .6), title='Результат', title_align='center',
                                 title_size=20, content=content)
        content.add_widget(Label(text=calculation.label))
        content.add_widget(Label(text=f'Общее: {str(calculation.overall_score)}', font_size=25))
        content.add_widget(Button(text='Закрыть', on_press=self.popup_count.dismiss, size_hint=[1, 0.6]))
        self.popup_count.open()

    def button_date_click(self, instance):
        content = GridLayout(cols=1, rows=3, padding=[10])

        content_datapicker = GridLayout(cols=3, rows=1, padding=[20, 0, 20, 10], spacing=10)

        self.data_picker_day = TextInput(text=self.day, multiline=False, font_size=26, halign='center',
                                         input_filter='int', padding=[0, 10])
        self.data_picker_month = TextInput(text=self.month, multiline=False, font_size=26, halign='center',
                                           input_filter='int', padding=[0, 10])
        self.data_picker_year = TextInput(text=self.year, multiline=False, font_size=26, halign='center',
                                          input_filter='int', padding=[0, 10])

        day_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        day_picker_layout.add_widget(Label(text='День', font_size=24))
        day_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.plus_day))
        day_picker_layout.add_widget(self.data_picker_day)
        day_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.minus_day))

        month_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        month_picker_layout.add_widget(Label(text='Месяц', font_size=24))
        month_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.plus_month))
        month_picker_layout.add_widget(self.data_picker_month)
        month_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.minus_month))

        year_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        year_picker_layout.add_widget(Label(text='Год', font_size=24))
        year_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.plus_year))
        year_picker_layout.add_widget(self.data_picker_year)
        year_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.minus_year))

        content_datapicker.add_widget(day_picker_layout)
        content_datapicker.add_widget(month_picker_layout)
        content_datapicker.add_widget(year_picker_layout)
        content.add_widget(content_datapicker)
        content.add_widget(
            Label(text=f'Текущая дата:\n{self.day} {month_dict[self.month]} {self.year}', size_hint=[1, .6]))

        buttons_layout = GridLayout(rows=1, cols=2, spacing=5, size_hint=[1, 0.3])
        buttons_layout.add_widget(Button(text='Сегодня ', on_press=self.reset_date))
        buttons_layout.add_widget(Button(text='Загрузить', on_press=self.load_date))
        content.add_widget(buttons_layout)

        self.popup_date = Popup(size_hint=(.8, .7), title='История', title_align='center',
                                title_size=20, content=content)

        self.popup_date.open()

    def plus_day(self, instance):
        result = self.data_picker_day._get_text()
        result = int(result) + 1
        if result <= 31:
            self.day = str(result)
        else:
            self.day = '1'
        self.data_picker_day._set_text(self.day)

    def minus_day(self, instance):
        result = self.data_picker_day._get_text()
        result = int(result) - 1
        if result > 0:
            self.day = str(result)
        else:
            self.day = '31'
        self.data_picker_day._set_text(self.day)

    def plus_month(self, instance):
        result = self.data_picker_month._get_text()
        result = int(result) + 1
        if result <= 12:
            self.month = str(result)
        else:
            self.month = '1'
        self.data_picker_month._set_text(self.month)

    def minus_month(self, instance):
        result = self.data_picker_month._get_text()
        result = int(result) - 1
        if result > 0:
            self.month = str(result)
        else:
            self.month = '12'
        self.data_picker_month._set_text(self.month)

    def plus_year(self, instance):
        result = self.data_picker_year._get_text()
        result = int(result) + 1
        self.year = str(result)
        self.data_picker_year._set_text(self.year)

    def minus_year(self, instance):
        result = self.data_picker_year._get_text()
        result = int(result) - 1
        self.year = str(result)
        self.data_picker_year._set_text(self.year)

    def load_date(self, instance):
        global date
        date = f'{self.year}-{self.month}-{self.day}'
        try:
            self.text_input.text = data.get('data')[date]
        except KeyError:
            data['data'][date] = ''
            self.text_input.text = data.get('data')[date]
        self.popup_date.dismiss()

    def reset_date(self, instance):
        global date
        self.day = datetime.datetime.strftime(datetime.datetime.now(), "%d")
        self.data_picker_day._set_text(self.day)
        self.month = datetime.datetime.strftime(datetime.datetime.now(), "%m")
        self.data_picker_month._set_text(self.month)
        self.year = datetime.datetime.strftime(datetime.datetime.now(), "%Y")
        self.data_picker_year._set_text(self.year)
        date = f'{self.year}-{self.month}-{self.day}'
        try:
            self.text_input.text = data.get('data')[date]
        except KeyError:
            data['data'][date] = ''
            self.text_input.text = data.get('data')[date]
        self.popup_date.dismiss()


def autosave():
    while autosave:
        time.sleep(0.5)
        buffer_dict = data['data']
        buffer_dict[date] = app.text_input._get_text()
        data['data'] = buffer_dict

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
