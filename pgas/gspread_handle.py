from typing import List

import gspread
from gspread import Worksheet, WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

from pgas.utils import range_grid


class GSpread:
    worksheet_rows = 15000
    worksheet_cols = 26

    def __init__(self, key_file, spreadsheet_url):
        self.gs = None
        self.authorization_on_google(key_file)

        self.spreadsheet = self.get_spreadsheet(spreadsheet_url)
        self.main_worksheet = None
        self.achievements_worksheet = None

    def authorization_on_google(self, key_file):
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
        self.gs = gspread.authorize(credentials)

    def get_spreadsheet(self, spreadsheet_url):
        return self.gs.open_by_url(spreadsheet_url)

    def share_access(self, email, role='writer'):
        self.spreadsheet.share(email, perm_type='user', role=role)

    def get_sheet(self, title: str) -> Worksheet:
        try:
            sheet = self.spreadsheet.worksheet(title)
        except WorksheetNotFound:
            sheet = self.spreadsheet.add_worksheet(title, self.worksheet_rows, self.worksheet_cols)
        return sheet

    def _get_ids(self, title: str) -> List[int]:
        worksheet = self.get_sheet(title)
        cells = worksheet.range(f'A2:A{self.worksheet_rows}')
        return [int(cell.value) for cell in cells if cell.value.isdigit()]

    def get_ids(self) -> List[int]:
        return self._get_ids('Список ID для выгрузки')

    def get_ids_last_pgas(self) -> List[int]:
        return self._get_ids('Список ID прошлого семестра')

    def fill_main_worksheet(self, data):
        worksheet = self.get_sheet('Общий список')
        worksheet.clear()

        cols = ['ID', 'ФИО', 'Баллы', 'Тип', 'Тип 273-ФЗ', 'Профиль']
        row_n, col_n = len(data) + 1, len(cols)
        cells = worksheet.range(range_grid((1, 1), (row_n, col_n)))
        curr = iter(cells)

        for columns in cols:
            next(curr).value = columns

        for user_id, user in sorted(data.items(), key=lambda x: x[1]['score'], reverse=True):
            next(curr).value = user_id
            next(curr).value = user['name']
            next(curr).value = user['score']
            next(curr).value = user['type']
            next(curr).value = user['type_273']
            next(curr).value = user['url']

        worksheet.update_cells(cells)

    def fill_achievements_worksheet(self, data):
        worksheet = self.get_sheet('Список достижений')
        worksheet.clear()

        cols = [
            'ID', 'ФИО', 'Тип', 'Категория', 'Название',
            'Балл', 'Дата получения', 'Проверено', 'Комментарий', 'Наш комментарий',
            'URL достижения', 'URL подтверждения',
        ]
        row_n, col_n = sum([len(user['achievements']) for user in data.values()]) + 1, len(cols)
        cells = worksheet.range(range_grid((1, 1), (row_n, col_n)))
        curr = iter(cells)

        for columns in cols:
            next(curr).value = columns

        for user_id, user in sorted(data.items(), key=lambda x: x[1]['name']):
            for achievement in user['achievements']:
                next(curr).value = user_id
                next(curr).value = user['name']
                next(curr).value = achievement['type']
                next(curr).value = achievement['category']
                next(curr).value = achievement['title']
                next(curr).value = achievement.get('score_our', achievement['score'])
                next(curr).value = achievement['date']
                next(curr).value = achievement['checked']
                next(curr).value = achievement['comment']
                next(curr).value = achievement['comment_our']
                next(curr).value = achievement['url']
                next(curr).value = achievement['file']

        worksheet.update_cells(cells)
