import gspread
from gspread import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials


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
            self.spreadsheet =  self.gs.open_by_url('https://docs.google.com/spreadsheets/d/'
                                                    '1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc')
        return self.spreadsheet

    def get_sheet(self, title):
        try:
            sheet = self.get_spreadsheet().worksheet(title)
        except WorksheetNotFound:
            sheet = self.get_spreadsheet().add_worksheet('Общий список', 5000, 26)
        return sheet

    def get_main_worksheet(self):
        if not self.main_worksheet:
            self.main_worksheet = self.get_sheet('Общий список')
        return self.main_worksheet

    def get_achievements_worksheet(self):
        if not self.achievements_worksheet:
            self.achievements_worksheet = self.get_sheet('Список достижений')
        return self.achievements_worksheet
