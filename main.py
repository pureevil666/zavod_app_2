from kivy.config import Config

Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 0)
Config.set('graphics', 'top', 0)
# Config.set('graphics', 'height', 900)

import calculation
import threading
import time
import datetime
import sys
import math
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
from kivy.uix.scrollview import ScrollView
from kivy.uix.carousel import Carousel

autosave = True
date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
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

if not 'data' in data:
    data.put('data')
if date in data['data']:
    text = data.get('data')[date]
else:
    text = ''
    data['data'][date] = text


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

        main_layout = GridLayout(rows=3, cols=1)
        self.date_label = Label(text=self.to_text_date(date), font_size=20, size_hint=[1, .03],
                                disabled_outline_color=[.17, .17, .17, 1])
        main_layout.add_widget(self.date_label)
        self.text_input = Input(text=text, background_color=[.17, .17, .17, 1], foreground_color=[.9, .9, .9, 1],
                                text_language='ru', font_size=28, padding=[10, 0, 10, 0])
        main_layout.add_widget(self.text_input)

        self.bottom_layout = GridLayout(rows=1, cols=3)
        self.button_count = Button(text='Посчитать', font_size=24, on_press=self.button_count_click)
        self.button_date = Button(text='Дата', font_size=24, on_press=self.button_date_click)
        self.button_history = Button(text='История', font_size=24, on_press=self.button_history_click)
        self.bottom_layout.add_widget(self.button_count)
        self.bottom_layout.add_widget(self.button_date)
        self.bottom_layout.add_widget(self.button_history)

        main_layout.add_widget(self.bottom_layout)
        return main_layout

    def button_count_click(self, instance):
        calculation.give_data(self.text_input._get_text())
        content = GridLayout(cols=1, rows=3, padding=[10])
        self.popup_count = Popup(size_hint=(.7, .6), title='Результат', title_align='center',
                                 title_size=28, content=content)
        content.add_widget(Label(text=calculation.label))
        content.add_widget(Label(text=f'Общее: {str(calculation.overall_score)}', font_size=26))
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

        self.popup_date = Popup(size_hint=(.8, .7), title='Дата', title_align='center',
                                title_size=28, content=content)

        self.popup_date.open()

    def button_history_click(self, instance):
        self.clear_history()
        self.buttons_list = []
        self.carousel_list = []
        self.data_lenght = len(data['data'])

        content = GridLayout(cols=1, rows=2, spacing=10, padding=[10])
        self.popup_history = Popup(size_hint=(.8, .9), title='История', title_align='center',
                                   title_size=28, content=content)

        buttons = GridLayout(cols=2, rows=1, spacing=5, size_hint=[1, .1])
        buttons.add_widget(Button(text='Очистить', font_size=26, size_hint=[1, .1], on_release=self.destroy_history))
        buttons.add_widget(
            Button(text='Закрыть', font_size=26, on_release=self.popup_history.dismiss))

        carousel = Carousel(direction='bottom')
        content.add_widget(carousel)
        content.add_widget(buttons)

        for el in self.data_names:
            el = el.split('-')
            name = f'{el[2]} {month_dict[el[1]]} {el[0]}'
            self.buttons_list.append(Button(text=str(name), font_size=24, on_release=self.load_history))

        for i in range(math.ceil(self.data_lenght / 20)):
            self.carousel_list.append(GridLayout(cols=1, rows=20, spacing=[2]))

        for car in self.carousel_list:
            count = 0
            while count < 20:
                try:
                    car.add_widget(self.buttons_list[count])
                except IndexError:
                    break
                count += 1
            self.buttons_list = self.buttons_list[count:]

        for el in self.carousel_list:
            carousel.add_widget(el)

        self.popup_history.open()

    def destroy_history(self, instance):
        self.popup_history.dismiss()
        for el in data['data']:
            if el != datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"):
                data['data'][el] = ''

    def clear_history(self):
        self.data_names = []
        for el in data['data']:
            self.data_names.append(el)
        for el in self.data_names:
            if data['data'][el] == '':
                del data['data'][el]
        self.data_names.clear()
        for el in data['data']:
            self.data_names.append(el)

    def load_history(self, instance):
        global date
        date = self.to_number_date(instance.text)
        self.text_input.text = data.get('data')[date]
        self.date_label.text = self.to_text_date(date)
        self.popup_history.dismiss()

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
        self.day = self.data_picker_day._get_text()
        self.month = self.data_picker_month._get_text()
        self.year = self.data_picker_year._get_text()
        date = f'{self.year}-{self.month}-{self.day}'
        try:
            self.text_input.text = data.get('data')[date]
        except KeyError:
            data['data'][date] = ''
            self.text_input.text = data.get('data')[date]
        self.date_label.text = self.to_text_date(date)
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
        self.date_label.text = self.to_text_date(date)
        self.popup_date.dismiss()

    def to_text_date(self, d):
        d = d.split('-')
        return f'{d[2]} {month_dict[d[1]]} {d[0]}'

    def to_number_date(self, d):
        d = d.split(' ')
        return f'{d[2]}-{get_key(month_dict, d[1])}-{d[0]}'


def autosave():
    while autosave:
        time.sleep(0.5)
        buffer_dict = data['data']
        buffer_dict[date] = app.text_input._get_text()
        data['data'] = buffer_dict

    sys.exit()


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


if __name__ == '__main__':
    app = MyApp()
    saver = threading.Thread(target=autosave)
    saver.start()
    app.run()

try:
    pass
finally:
    autosave = False
