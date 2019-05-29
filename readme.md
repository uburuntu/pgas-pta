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
* Ввод логина и пароля для сети Ломоносов: [passwords.py](pgas/passwords.py)
* Получение key.json для авторизации в Google: [console.developers.google.com](https://console.developers.google.com/)
* Выставление аргументов в [main.py](main.py)
* Указание в листах целевого spreadsheet ID для выгрузки и ID прошлого семестра
* Запуск скрипта: `python main.py`

#### Подробный мануал от пользователей:
1. Установить Python 3.6 или выше
1. Скачать репозиторий с помощью Github Desktop (Windows) или `git clone https://github.com/uburuntu/pgas-pta` (Linux)
1. Запустить терминал (в Windows командную строку или Windows PowerShell)
1. Перейти в директорию репозитория `cd C:\Users\{название профиля}\Documents\Github\pgas-pta` (Windows) и `cd pgas-pta` (Linux)
1. Установить необходимых модулей: `pip install -r requirements.txt`
1. Ввод логина и пароля аккаунта с редакторскими правами для сети Ломоносов: `passwords.py`
1. Получение `key.json` для авторизации в Google: https://console.developers.google.com
1. Выставление аргументов в `main.py`:
   * `date_one_year` (дата, с которой принимаются достижения в этом распределении)
   * `date_last_pgas` (дата, по которую принимались достижения в прошлом распределении)
   * `google_spreadsheet_link` (ссылка на таблицу для выгрузки результатов)
   * `google_key_filename` (путь к key.json для авторизации)
   * `force_update_achievements` (True для обновления достижений с портала, иначе использует предыдущие запуски)
   * `count_score_with_unchecked_achievements` (True для учета всех достижений, False для учета только проверенных)
1. Настроить в таблице [pgas-pta](https://docs.google.com/spreadsheets/d/10zX0UM1x6YeU5vj1DuLR0RtHF3_Zas7No1jJSu8gOd8/edit#gid=0) доступ к таблице анкеты текущего распределения  
1. Запуск скрипта: `python main.py`
1. Результаты смотрим по ссылке в `google_spreadsheet_link`
