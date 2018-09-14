# pgas-pta

Система для автоматической обработки и выгрузки достижений в сети Ломоносов ([lomonosov-msu.ru](https://lomonosov-msu.ru)).

##### Этапы:
1. Парсинг страниц профилей
1. Парсинг страниц достижений
1. Накладывание определенных фильтров
1. Выгрузка получившихся данных в Google Spreadsheets

##### Ключи:
* Ввод логина и пароля для сети Ломоносов: [passwords.py](passwords.py)
* Получение key.json для авторизации в Google: [console.developers.google.com](https://console.developers.google.com/)
