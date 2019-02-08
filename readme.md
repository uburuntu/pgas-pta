# pgas-pta

[![Python ⩾ 3.6](https://img.shields.io/badge/Python-⩾-3.6-blue.svg?longCache=true)]()

Система для автоматической обработки достижений в сети Ломоносов ([lomonosov-msu.ru](https://lomonosov-msu.ru)).

#### Этапы:
1. Парсинг страниц профилей
1. Парсинг страниц достижений  
1. Накладывание определенных фильтров
1. Дополнительные вычисления согласно системе ПГАС Студсовета
1. Выгрузка получившихся данных в Google Spreadsheets

#### Запуск:
* Установка необходимых модулей: `pip install -r requirements.txt`
* Выставление аргументов в [main.py](main.py)
* Ввод логина и пароля для сети Ломоносов: [passwords.py](pgas/passwords.py)
* Получение key.json для авторизации в Google: [console.developers.google.com](https://console.developers.google.com/)
* Создание файла `users.txt` с id претендентов из сети Ломоносов
* Запуск скрипта: `python main.py`
