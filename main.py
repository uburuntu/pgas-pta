import passwords
from gspread_handle import GSpread
from lmsu_handle import LomonosovMSU
from utils import print_section

if __name__ == '__main__':
    #
    # Script arguments
    #
    lmsu_data_from_file = True
    users_filename = 'users.csv'
    google_key_filename = 'key.json'

    #
    # MSU
    #
    lmsu = LomonosovMSU()

    if lmsu_data_from_file:
        print_section('Loading data from file')
        lmsu.load()
    else:
        print_section('Connecting to Lomonosov network')
        lmsu.authorization_on_msu(username=passwords.auth_login, password=passwords.auth_pswd)

        print_section('Collecting users info')
        lmsu.scrap_data(users_filename)

        print_section(f'Collecting {len(lmsu.data)} user(s) achievements')
        lmsu.scrap_achievements()

    print_section(f'Filtering {len(lmsu.data)} user(s)')
    lmsu.filter_users()

    print_section(f'Dumping users data to file')
    lmsu.dump()

    #
    # Google table
    #
    print_section('Connecting to Google Spreadsheets')
    gspread = GSpread(google_key_filename)

    print_section('Filling main worksheet with our data')
    gspread.fill_main_worksheet(lmsu.data)

    print_section('Filling achievements with our data')
    gspread.fill_achievements_worksheet(lmsu.data)
