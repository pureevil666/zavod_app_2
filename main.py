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
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore
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
month_dict_fullname = {
    '1': 'Январь',
    '2': 'Февраль',
    '3': 'Март',
    '4': 'Апрель',
    '5': 'Май',
    '6': 'Июнь',
    '7': 'Июль',
    '8': 'Август',
    '9': 'Сентябрь',
    '10': 'Октябрь',
    '11': 'Ноябрь',
    '12': 'Декабрь',
}

if not date in data:
    data.put(date)
if 'text' in data[date]:
    text = data.get(date)['text']
else:
    text = ''
    data[date]['text'] = text


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


class DateInput(TextInput):
    def __init__(self, text):
        super(DateInput, self).__init__()
        self.text = text
        self.multiline = False
        self.font_size = 26
        self.halign = 'center'
        self.input_filter = 'int'
        self.padding = [0, 10]


class MyApp(App):
    def build(self):
        self.day = datetime.datetime.strftime(datetime.datetime.now(), "%d")
        self.month = datetime.datetime.strftime(datetime.datetime.now(), "%m")
        self.year = datetime.datetime.strftime(datetime.datetime.now(), "%Y")

        main_layout = GridLayout(rows=3, cols=1)
        self.date_label = Label(text=self.to_text_date(date), font_size=20, size_hint=[1, .03])
        self.text_input = Input(text=text, background_color=[.17, .17, .17, 1], foreground_color=[.9, .9, .9, 1],
                                text_language='ru', font_size=28, padding=[10, 0, 10, 0])

        self.bottom_layout = GridLayout(rows=1, cols=3)
        self.button_count = Button(text='Посчитать', font_size=24, on_press=self.button_count_click)
        self.button_date = Button(text='Дата', font_size=24, on_press=self.button_date_click)
        self.button_history = Button(text='История', font_size=24, on_press=self.button_history_click)
        self.bottom_layout.add_widget(self.button_count)
        self.bottom_layout.add_widget(self.button_date)
        self.bottom_layout.add_widget(self.button_history)

        main_layout.add_widget(self.date_label)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(self.bottom_layout)
        return main_layout

    def button_count_click(self, instance):
        calculation.give_data(self.text_input._get_text())
        data[date]['result'] = calculation.overall_score
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

        self.data_picker_day = DateInput(self.day)
        self.data_picker_month = DateInput(self.month)
        self.data_picker_year = DateInput(self.year)

        day_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        day_picker_layout.add_widget(Label(text='День', font_size=24))
        day_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.change_day))
        day_picker_layout.add_widget(self.data_picker_day)
        day_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.change_day))

        month_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        month_picker_layout.add_widget(Label(text='Месяц', font_size=24))
        month_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.change_month))
        month_picker_layout.add_widget(self.data_picker_month)
        month_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.change_month))

        year_picker_layout = GridLayout(cols=1, rows=4, padding=[10, 0])
        year_picker_layout.add_widget(Label(text='Год', font_size=24))
        year_picker_layout.add_widget(Button(text='+', font_size=24, on_press=self.change_year))
        year_picker_layout.add_widget(self.data_picker_year)
        year_picker_layout.add_widget(Button(text='-', font_size=24, on_press=self.change_year))

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
        self.sort_history()
        self.buttons_list = []
        self.carousel_list = []
        self.data_lenght = len(data)

        content = GridLayout(cols=1, rows=2, spacing=10, padding=[10])
        self.popup_history = Popup(size_hint=(.8, .9), title='История', title_align='center',
                                   title_size=28, content=content)

        buttons = GridLayout(cols=3, rows=1, spacing=5, size_hint=[1, .1])
        buttons.add_widget(Button(text='Очистить', font_size=26, size_hint=[1, .1], on_release=self.destroy_history))
        buttons.add_widget(Button(text='Статистика', font_size=26, size_hint=[1, .1], on_release=self.show_statistic))
        buttons.add_widget(Button(text='Закрыть', font_size=26, on_release=self.popup_history.dismiss))

        carousel = Carousel(direction='bottom')
        content.add_widget(carousel)
        content.add_widget(buttons)

        for el in self.data_names:
            result = ''
            if 'result' in data[el]:
                if data[el]['result'] > 0:
                    result += f'    ({data[el]["result"]})'
            el = self.to_text_date(el)
            self.buttons_list.append(Button(text=f"{el}{result}", font_size=24, on_release=self.load_history))

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
        for el in data:
            if el != datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d"):
                data[el]['text'] = ''

    def clear_history(self):
        self.data_names = []
        for el in data:
            self.data_names.append(el)
        for el in self.data_names:
            if data[el]['text'] == '':
                data.delete(el)
        self.data_names.clear()
        for el in data:
            self.data_names.append(el)

    def load_history(self, instance):
        global date
        date = self.to_number_date(instance.text)
        self.text_input.text = data.get(date)['text']
        self.date_label.text = self.to_text_date(date)
        self.popup_history.dismiss()

    def sort_history(self):
        new_array = []
        out_array = []
        new_dict = {}
        for el in self.data_names:
            arr = el.split('-')
            new_dict[10000*int(arr[0]) + 100*int(arr[1]) + int(arr[2])] = el
        for key, val in new_dict.items():
            new_array.append(key)
        new_array.sort(reverse=True)
        for el in new_array:
            out_array.append(new_dict[el])
        self.data_names = out_array

    def show_statistic(self, instance):
        self.popup_history.dismiss()
        self.get_month_list()
        stat_content = GridLayout(cols=1, rows=2, padding=[10])
        self.popup_statistics = Popup(size_hint=(.8, .9), title='Статистика', title_align='center',
                                      title_size=28, content=stat_content)

        stat_carousel = Carousel(direction='bottom')
        stat_content.add_widget(stat_carousel)
        stat_buttons = GridLayout(cols=2, rows=1, padding=[5], size_hint=[1, 0.1])
        stat_buttons.add_widget(Button(text='Закрыть', font_size=26, on_release=self.popup_statistics.dismiss))
        stat_content.add_widget(stat_buttons)

        buttons_list = []
        carousel_list = []
        for el in self.month_list:
            buttons_list.append(Button(text=str(el), font_size=24, on_release=self.show_month_statistics))

        for i in range(math.ceil(len(self.month_list) / 10)):
            carousel_list.append(GridLayout(cols=1, rows=10, spacing=[2]))

        for car in carousel_list:
            count = 0
            while count < 10:
                try:
                    car.add_widget(buttons_list[count])
                except IndexError:
                    break
                count += 1
            buttons_list = buttons_list[count:]

        for el in carousel_list:
            stat_carousel.add_widget(el)

        self.popup_statistics.open()

    def show_month_statistics(self, instance):
        self.popup_statistics.dismiss()

        content = GridLayout(rows=2, cols=1)
        self.popup_statistics_month = Popup(size_hint=(.5, .6), title='Статистика', title_align='center',
                                      title_size=28, content=content)
        result_text = self.count_statistics(instance.text)
        content_text_layout = GridLayout(rows=2, cols=1)
        content_result_text = Label(text=result_text, font_size=24)
        content_label_text = Label(text=f'Результат за\n{instance.text}', font_size=28)
        content_text_layout.add_widget(content_label_text)
        content_text_layout.add_widget(content_result_text)
        content_buttons = GridLayout(rows=1, cols=2, size_hint=[1, .1], padding=[5])
        content_buttons.add_widget(Button(text='Назад', font_size=26, on_release=self.back_button))
        content_buttons.add_widget(Button(text='Закрыть', font_size=26, on_release=self.popup_statistics_month.dismiss))
        content.add_widget(content_text_layout)
        content.add_widget(content_buttons)

        self.popup_statistics_month.open()

    def back_button(self, instance):
        self.popup_statistics_month.dismiss()
        self.popup_statistics.open()

    def get_month_list(self):
        self.month_list = []
        for el in self.data_names:
            buf = el.split('-')
            if not f'{month_dict_fullname[buf[1]]} {buf[0]}' in self.month_list:
                self.month_list.append(f'{month_dict_fullname[buf[1]]} {buf[0]}')
        print(self.month_list)

    def count_statistics(self, value):
        month = get_key(month_dict_fullname, value.split(' ')[0])
        year = value.split(' ')[1]
        result = 0
        money = 0
        yearmonth = f'{year}-{month}'
        for el in data:
            if yearmonth in el:
                if 'result' in data[el]:
                    result += data[el]['result']

        return str(f'Количество: {result} шт.\nЗаработано: {money}')

    def change_day(self, instance):
        result = self.data_picker_day._get_text()
        result = int(eval(f'{result}{instance.text}1'))
        if result > 31:
            self.day = '1'
        elif result == 0:
            self.day = '31'
        else:
            self.day = str(result)

        self.data_picker_day._set_text(self.day)

    def change_month(self, instance):
        result = self.data_picker_month._get_text()
        result = int(eval(f'{result}{instance.text}1'))
        if result > 12:
            self.month = '1'
        elif result < 1:
            self.month = '12'
        else:
            self.month = str(result)
        self.data_picker_month._set_text(self.month)

    def change_year(self, instance):
        result = self.data_picker_year._get_text()
        result = int(eval(f'{result}{instance.text}1'))
        self.year = str(result)
        self.data_picker_year._set_text(self.year)

    def load_date(self, instance):
        global date
        self.day = self.data_picker_day._get_text()
        self.month = self.data_picker_month._get_text()
        self.year = self.data_picker_year._get_text()
        date = f'{self.year}-{self.month}-{self.day}'
        try:
            self.text_input.text = data.get(date)['text']
        except KeyError:
            data.put(date)
            data[date]['text'] = ''
            self.text_input.text = data.get(date)['text']
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
            self.text_input.text = data.get(date)['text']
        except KeyError:
            data.put(date)
            data[date]['text'] = ''
            self.text_input.text = data.get(date)['text']
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
        if not date in data:
            data.put(date)
        buffer_dict = data[date]
        buffer_dict['text'] = app.text_input._get_text()
        data[date] = buffer_dict
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
