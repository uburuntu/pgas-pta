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
        print_subsection('Filling header')
        cells = worksheet.range(range_grid((1, 1), (1, 5)))
        cells[0].value = 'ID'
        cells[1].value = 'ФИО'
        cells[2].value = 'Номер группы'
        cells[3].value = 'Баллы'
        cells[4].value = 'URL'

        curr_line = 2
        for user_id, user in data.items():
            print_subsection(f'Filling user {user_id} data — {user["name"]}')
            cells = worksheet.range(range_grid((curr_line, 1), (curr_line, 5)))
            cells[0].value = user_id
            cells[1].value = user['name']
            cells[2].value = 'хз'
            cells[3].value = sum([int(x['score']) for x in user['achievements']])
            cells[4].value = f'http://lomonosov-msu.ru/rus/user/achievement/user/{user_id}/list'
            curr_line += 1

        cells = worksheet.range(range_grid((1, 1), (curr_line, 8)))
        worksheet.update_cells(cells)

    def fill_achievements_worksheet(self, data):
        worksheet = self.get_achievements_worksheet()
        print_subsection('Filling header')
        cells = worksheet.range(range_grid((1, 1), (1, 8)))
        cells[0].value = 'ID'
        cells[1].value = 'ФИО'
        cells[2].value = 'Название'
        cells[3].value = 'Категория'
        cells[4].value = 'Дата получения'
        cells[5].value = 'Балл'
        cells[6].value = 'URL достижения'
        cells[7].value = 'URL подтверждения'

        curr_line = 2
        for user_id, user in data.items():
            print_subsection(f'Filling user {user_id} achievements — {user["name"]}')
            for achievement in user['achievements']:
                cells = worksheet.range(range_grid((curr_line, 1), (curr_line, 8)))
                cells[0].value = user_id
                cells[1].value = user['name']
                cells[2].value = achievement['title']
                cells[3].value = achievement['category']
                cells[4].value = achievement['date']
                cells[5].value = achievement['score']
                cells[6].value = achievement['url']
                cells[7].value = achievement['file']
                curr_line += 1

        cells = worksheet.range(range_grid((1, 1), (curr_line, 8)))
        worksheet.update_cells(cells)
