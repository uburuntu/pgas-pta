# pgas-pta

Система для автоматической обработки достижений в сети Ломоносов ([lomonosov-msu.ru](https://lomonosov-msu.ru)).

#### Этапы:
1. Парсинг страниц профилей
1. Парсинг страниц достижений  
1. Накладывание определенных фильтров
1. Дополнительные вычисления согласно системе ПГАС Студсовета
1. Выгрузка получившихся данных в Google Spreadsheets


#### Используемые модули:
* **waylan** / [beautifulsoup](https://github.com/waylan/beautifulsoup)
* **lorien** / [grab](https://github.com/lorien/grab)
* **burnash** / [gspread](https://github.com/burnash/gspread)
* **googleapis** / [oauth2client](https://github.com/googleapis/oauth2client)


#### Запуск:
* Выставление аргументов в [main.py](main.py)
* Ввод логина и пароля для сети Ломоносов: [passwords.py](pgas/passwords.py)
* Получение key.json для авторизации в Google: [console.developers.google.com](https://console.developers.google.com/)
* Создание файла users.csv с id претендентов из сети Ломоносов
