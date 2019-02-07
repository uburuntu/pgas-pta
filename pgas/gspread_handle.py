import gspread
from gspread import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

from pgas.utils import range_grid


class GSpread:
    def __init__(self, key_file):
        self.gs = None
        self.authorization_on_google(key_file)

        self.spreadsheet = None

        self.main_worksheet = None
        self.achievements_worksheet = None

    def authorization_on_google(self, key_file):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
        self.gs = gspread.authorize(credentials)

    def get_spreadsheet(self):
        if not self.spreadsheet:
            self.spreadsheet = self.gs.open_by_url('https://docs.google.com/spreadsheets/d/1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc')
        return self.spreadsheet

    def share_access(self, email, role='writer'):
        self.get_spreadsheet().share(email, perm_type='user', role=role)

    def get_sheet(self, title):
        try:
            sheet = self.get_spreadsheet().worksheet(title)
        except WorksheetNotFound:
            sheet = self.get_spreadsheet().add_worksheet(title, 15000, 26)
        return sheet

    def get_main_worksheet(self):
        if not self.main_worksheet:
            self.main_worksheet = self.get_sheet('Общий список')
        return self.main_worksheet

    def get_achievements_worksheet(self):
        if not self.achievements_worksheet:
            self.achievements_worksheet = self.get_sheet('Список достижений')
        return self.achievements_worksheet

    def fill_main_worksheet(self, data):
        worksheet = self.get_main_worksheet()

        row_n, col_n = len(data) + 1, 7
        cells = worksheet.range(range_grid((1, 1), (row_n, col_n)))
        curr = iter(cells)

        next(curr).value = 'ID'
        next(curr).value = 'ФИО'
        next(curr).value = 'Номер группы'
        next(curr).value = 'Баллы'
        next(curr).value = 'Тип'
        next(curr).value = 'Тип 273-ФЗ'
        next(curr).value = 'URL'

        for user_id, user in data.items():
            next(curr).value = user_id
            next(curr).value = user['name']
            next(curr).value = 'n/a'
            next(curr).value = user['score']
            next(curr).value = user['type']
            next(curr).value = user['type_273']
            next(curr).value = user['url']

        worksheet.update_cells(cells)

    def fill_achievements_worksheet(self, data):
        worksheet = self.get_achievements_worksheet()

        row_n, col_n = sum([len(user['achievements']) for user in data.values()]) + 1, 10
        cells = worksheet.range(range_grid((1, 1), (row_n, col_n)))
        curr = iter(cells)

        next(curr).value = 'ID'
        next(curr).value = 'ФИО'
        next(curr).value = 'Тип'
        next(curr).value = 'Категория'
        next(curr).value = 'Название'
        next(curr).value = 'Балл'
        next(curr).value = 'Дата получения'
        next(curr).value = 'Проверено'
        next(curr).value = 'URL достижения'
        next(curr).value = 'URL подтверждения'

        for user_id, user in data.items():
            for achievement in user['achievements']:
                next(curr).value = user_id
                next(curr).value = user['name']
                next(curr).value = achievement['type']
                next(curr).value = achievement['category']
                next(curr).value = achievement['title']
                next(curr).value = achievement['score']
                next(curr).value = achievement['date']
                next(curr).value = achievement['checked']
                next(curr).value = achievement['url']
                next(curr).value = achievement['file']

        worksheet.update_cells(cells)
