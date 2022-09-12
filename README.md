## About
<p>Standalone приложения для Win и Linux.</p>
<p>Позволяет узнать базовые характеристики компьютера и сети.</p>
<p>Так же есть возможность произвести поиск необходимых программ
(определяется внутри кода, а не пользователем.</p>
<p>После выбора отсутствующих программ выполняется "функция-затычка"
(функционал по установке ПО не реализован)</p>
<p>Результаты записываются в отдельный виджет и при желании можно реализовать экспорт данных
через отправку по e-mail или сервис API.</p>

## Documentation
<h3>Linux:</h3>
<p>pyinstaller app_byod.py --onefile</p>
<p>staticx app_byod app_byod_static</p>
<p>strip app_byod_static</p>
<h3>Windows:</h3>
<p>auto-py-to-exe</p>
<p>or</p>
<p>pyinstaller --noconfirm --onefile --windowed</p>

## License
MIT
