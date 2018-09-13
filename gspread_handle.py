import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GSpread:
    def __init__(self, key_file):
        self.gs = None
        self.authorization_on_google(key_file)

    def authorization_on_google(self, key_file):
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
        self.gs = gspread.authorize(credentials)

    def get_spreadsheet(self):
        return self.gs.open_by_url('https://docs.google.com/spreadsheets/d/'
                                   '1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc')

    def get_worksheet(self):
        return self.get_spreadsheet().get_worksheet(0)
