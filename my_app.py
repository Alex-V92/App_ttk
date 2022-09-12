from tkinter import *
import ttkbootstrap as ttk
from tkinter import scrolledtext, messagebox
from data import ComputerConfigMixin
import threading


class MyApp(ComputerConfigMixin):

    def __init__(self):
        # Словарь с набором функций для кнопки "Запуск"
        self.dict_command_func = {
            0: self.network,
            1: self.search_programs,
            2: self.install_func
        }

        # Словарь с набором описаний функций для кнопки "Запуск"
        self.dict_command_doc = {
            0: 'Проверка состояния сети',
            1: 'Поиск необходимых программ',
            2: 'Установка выбранных программ',
        }

        self.step = 0
        self.necessary_programs = True
        self.check_programs_is_run = False

        self.root = ttk.Window(themename='superhero')

        # Минимальные размеры полей для корректного бесшовного отображения разных виджетов
        self.root.grid_rowconfigure(2, minsize=380)
        self.root.grid_columnconfigure(0, minsize=550)

        self.root.wm_title("Тестовое приложение")

        self.bar = ttk.Progressbar(self.root, mode='indeterminate', )
        self.bar.grid(column=0, row=6, sticky='wens', pady=5, padx=5)
        self.bar['value'] = 0

        self.button_func = ttk.Button(
            text='Запуск',
            command=lambda: threading.Thread(target=self.dict_command_func[self.step], ).start(),
            width=8)
        self.button_func.grid(row=5,
                              column=0,
                              sticky='e',
                              pady=3,
                              padx=3,
                              )

        self.doc_button = Label(self.root, text=f'{self.dict_command_doc[self.step]} --->', padx=5, pady=5)
        self.doc_button.grid(row=5, column=0, sticky='w')

        self.button_back = ttk.Button(
            text='Назад',
            command=lambda: [self.click_button_back(), self.show_button_dock()],
            width=8)
        self.button_back.grid(row=7,
                              column=0,
                              sticky='w',
                              pady=3,
                              padx=3
                              )

        self.button_next = ttk.Button(
            text='Далее>>',
            command=lambda: [self.click_button_next(), self.show_button_dock()],

            width=8,
            state=DISABLED)
        self.button_next.grid(row=7,
                              column=0,
                              sticky='e',
                              pady=3,
                              padx=3,
                              )

        # Первоначальное текстовое поле
        self.txt = scrolledtext.ScrolledText(self.root, width=80, height=20, relief=SOLID, wrap=WORD, )
        self.txt.grid(column=0, row=2, pady=8, padx=8, )

        self.bar.start()

        self.frame_check = ttk.LabelFrame(self.root, bootstyle="default",
                                          text='Выберите программы для выполнения автоустановки',

                                          )
        self.frame_check.grid(row=2, column=0, sticky='wsen', pady=20, padx=20, )

        self.frame_check.grid_remove()

        if self.requirements()[1]:
            self.txt.insert(1.0, 'Ваш компьютер соответствует минимальным системным требованиям.\n'
                                 f'{self.requirements()[0]}'
                                 '------------------------------------------------------------------------------\n'
                            )
        else:
            self.txt.insert(1.0, f'Ваш компьютер не соответствует минимальным системным требованиям:\n'
                                 f'{self.requirements()[0]}\n'
                                 '------------------------------------------------------------------------------\n'
                            )
            messagebox.showerror('Системные требования',
                                 'Ваш компьютер не соответствует минимальным системным требованиям')
            self.button_next.configure(state=DISABLED)
            self.button_func.configure(state=DISABLED)
        self.bar.stop()
        self.button_back.configure(state=DISABLED)
        self.root.mainloop()

    def click_button_next(self) -> None:
        """
        Функция для действий кнопки "Далее>>".
        Увеличивает текущий шаг программы(self.step).
        :return:
            Возвращаемый результат зависит от текущего шага программы(self.step).
            Неактивна при достижении максимального шага.
        """
        self.step += 1
        self.button_back.configure(state=ACTIVE)
        if self.step == 1:
            if not self.check_programs_is_run:
                self.button_next.configure(state=DISABLED)
            elif self.necessary_programs:
                self.button_next.configure(text='Выход', command=self.root.destroy)
        if self.step == 2:
            self.suggest_install_programs()
            self.button_next.configure(state=DISABLED)

    def click_button_back(self) -> None:
        """
        Функция для действий кнопки "Назад".
        Уменьшает текущий шаг программы(self.step).
        :return:
            Возвращаемый результат зависит от текущего шага программы(self.step).
            Неактивна при достижении минимального шага.
        """
        self.step -= 1
        self.button_next.configure(state=ACTIVE)
        if self.step == 0:
            self.button_back.configure(state=DISABLED)
        if self.step < 2:
            self.frame_check.grid_remove()
            self.txt.grid()

    def show_button_dock(self) -> None:
        """
        Показывает описание текущего действия кнопки "Запуск".
        :return:
            Значение словаря self.dict_command_doc, ключем которого является текущий шаг программы(self.step).
        """
        self.doc_button.configure(text=f'{self.dict_command_doc[self.step]} --->', padx=5, pady=5)

    def network(self) -> None:
        """
        Функция для проверки текущего соединения с google.ru.
        Проверяет скорость загрузки и джиттер.
        :return:
            При успешном измерении делает запись в текстовое поле self.txt с полученными значениями.
            При невозможности измерения выдаёт ошибку messagebox.showerror.
        """
        self.bar.start()
        try:
            messagebox.showinfo('Проверка сети', 'Пожалуйста, завершите все активные сетевые '
                                                 'соединения для корректной проверки сети')
            result = self.get_network_speed()
            self.txt.configure(state=NORMAL)
            self.txt.insert(INSERT, 'Текущие показатели сети:\n'
                                    f'Скорость загрузки с google.ru - {result[0]}Mbps\n'
                                    f'Показатель джиттера - {result[1]}ms\n'
                                    '------------------------------------------------------------------------------\n')
            self.txt.configure(state=DISABLED)
            self.button_next.configure(state=ACTIVE)
        except:
            messagebox.showerror('Проверка сети', 'Пожалуйста, проверьте состояние сети '
                                                  'и попробуйте запустить проверку ещё раз')
        self.bar.stop()

    def search_programs(self) -> None:
        """
        Поиск заранее известных программ из модуля data.py(переменные chrome_version, node_version, vsc_version и
        dot_net_version, если это win)
        :return:
            После выполнения поиска записывает полученные значения в текстовое поле self.txt.
            Если программа не найдено, то в значении будет указано "НЕ НАЙДЕНО".
            При полном соответствие всех необходимых программ кнопка "Далее" изменяется на "Выход", а кнопка
            "Назад" становится неактивной.
        """
        self.bar.start()
        self.txt.configure(state=NORMAL)
        messagebox.showinfo('Проверка наличия программ',
                            'Выполняется проверка всех необходимых программ')
        result = self.programs()
        if not result[1]:
            self.necessary_programs = False
            messagebox.showwarning('Проверка наличия программ',
                                   'Не найдено всё необходимое ПО')

        else:
            messagebox.showinfo('Проверка наличия программ',
                                'Найдено всё необходимое ПО\n'
                                )
            messagebox.showinfo('Полная проверка',
                                'Оборудование полностью соответствует всем параметрам')

        self.txt.insert(INSERT, 'Текущий список ПО и их версии:\n'
                                f'{result[0]}'
                                '------------------------------------------------------------------------------\n')
        self.txt.configure(state=DISABLED)
        self.bar.stop()
        self.check_programs_is_run = True
        if not self.necessary_programs:
            self.button_next.configure(state=ACTIVE)
        else:
            self.button_back.configure(state=DISABLED)
            self.button_next.configure(text='Выход', command=self.root.destroy, state=ACTIVE)

    def suggest_install_programs(self) -> None:
        """
        Отображение чек-боксов с ненайденными программами с предложением установить их.
        Список ненайденных программ берётся из ComputerConfigMixin().programs()[2].
        :return:
            Виджет LabelForm с контейнерами, которые состоят из чек-боксов с предложением автоустановки
            указанных программ.
        """
        self.check_programs_is_run = True
        self.txt.grid_remove()
        self.frame_check.grid()

        self.programs_check_box = {}
        if 'chrome' in self.programs()[2]:
            self.value_chrome = StringVar()
            self.c1 = ttk.Checkbutton(self.frame_check,
                                      bootstyle="square-toggle",
                                      variable=self.value_chrome,
                                      onvalue='Google Chrome',
                                      offvalue='',
                                      text='Google Chrome',
                                      compound=LEFT,
                                      )
            self.c1.grid(row=0, column=0, sticky='w', padx=5, pady=10)

            self.programs_check_box['Google Chrome'] = self.value_chrome

        if 'node.js' in self.programs()[2]:
            self.node_js = StringVar()
            self.c2 = ttk.Checkbutton(self.frame_check,
                                      bootstyle="square-toggle",
                                      variable=self.node_js,
                                      onvalue='Node.js',
                                      offvalue='',
                                      text='Node.js',
                                      compound=LEFT,
                                      )
            self.c2.grid(row=1, column=0, sticky='w', padx=5, pady=10)

            self.programs_check_box['Node.js'] = self.node_js

        if 'vsc' in self.programs()[2]:
            self.vsc = StringVar()
            self.c3 = ttk.Checkbutton(self.frame_check,
                                      bootstyle="square-toggle",
                                      variable=self.vsc,
                                      onvalue='Visual Studio Code',
                                      offvalue='',
                                      text='Visual Studio Code',
                                      compound=LEFT,
                                      )

            self.c3.grid(row=2, column=0, sticky='w', padx=5, pady=10)

            self.programs_check_box['Visual Studio Code'] = self.vsc

        if 'dot_net' in self.programs()[2]:
            self.value_dot_net = StringVar()
            self.c4 = ttk.Checkbutton(self.frame_check,
                                      bootstyle="square-toggle",
                                      variable=self.value_dot_net,
                                      onvalue=".Net 4.8",
                                      offvalue='',
                                      text='.Net 4.8',
                                      compound=LEFT,
                                      )
            self.c4.grid(row=3, column=0, sticky='w', padx=5, pady=10)

            self.programs_check_box['.Net 4.8'] = self.value_dot_net

    def install_func(self) -> None:
        """
        Функция-заглушка для имитации начала запуска автоматической установки указанных программ.
        :return:
            messagebox.showinfo о начале установки либо о том, что ни одна из предложенных программ
            не выбрана.
        """

        def message_check_button() -> str:
            result = ''
            for key, value in self.programs_check_box.items():
                if value.get():
                    result += key + '\n'
            return result

        if message_check_button():
            messagebox.showinfo('ПО', 'Сейчас будет выполнена установка выбранного ПО:\n'
                                      f'{message_check_button()}'
                                )
        else:
            messagebox.showinfo('ПО', 'Не выбрана ни одна программа ')


if __name__ == '__main__':
    MyApp()
