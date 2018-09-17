import gspread
from gspread import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

from utils import print_subsection, range_grid


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
            self.spreadsheet = self.gs.open_by_url('https://docs.google.com/spreadsheets/d/'
                                                   '1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc')
        return self.spreadsheet

    def share_access(self, email, role='writer'):
        self.get_spreadsheet().share(email, perm_type='user', role=role)

    def get_sheet(self, title):
        try:
            sheet = self.get_spreadsheet().worksheet(title)
        except WorksheetNotFound:
            sheet = self.get_spreadsheet().add_worksheet(title, 5000, 26)
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

        row_n, col_n = len(data) + 1, 5
        curr_row = 1
        cells = worksheet.range(range_grid((curr_row, 1), (row_n, col_n)))

        row = cells[(curr_row - 1) * col_n:]
        row[0].value = 'ID'
        row[1].value = 'ФИО'
        row[2].value = 'Номер группы'
        row[3].value = 'Баллы'
        row[4].value = 'URL'
        curr_row += 1

        for user_id, user in data.items():
            row = cells[(curr_row - 1) * col_n:]
            row[0].value = user_id
            row[1].value = user['name']
            row[2].value = 'n/a'
            row[3].value = sum([int(x['score']) for x in user['achievements']])
            row[4].value = user['url']
            curr_row += 1

        worksheet.update_cells(cells)

    def fill_achievements_worksheet(self, data):
        worksheet = self.get_achievements_worksheet()

        row_n, col_n = sum([len(user['achievements']) for user in data.values()]) + 1, 8
        curr_row = 1
        cells = worksheet.range(range_grid((curr_row, 1), (row_n, col_n)))

        row = cells[(curr_row - 1) * col_n:]
        row[0].value = 'ID'
        row[1].value = 'ФИО'
        row[2].value = 'Название'
        row[3].value = 'Категория'
        row[4].value = 'Дата получения'
        row[5].value = 'Балл'
        row[6].value = 'URL достижения'
        row[7].value = 'URL подтверждения'
        curr_row += 1

        for user_id, user in data.items():
            for achievement in user['achievements']:
                row = cells[(curr_row - 1) * col_n:]
                row[0].value = user_id
                row[1].value = user['name']
                row[2].value = achievement['title']
                row[3].value = achievement['category']
                row[4].value = achievement['date']
                row[5].value = achievement['score']
                row[6].value = achievement['url']
                row[7].value = achievement['file']
                curr_row += 1

        worksheet.update_cells(cells)
