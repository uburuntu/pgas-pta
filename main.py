import passwords
from gspread_handle import GSpread
from lmsu_handle import LomonosovMSU
from utils import print_section, print_subsection, range_grid

if __name__ == '__main__':
    # MSU
    lmsu = LomonosovMSU()
    data_from_file = False

    if data_from_file:
        print_section('Loading data from file')
        lmsu.load()
    else:
        print_section('Connecting to Lomonosov network')
        lmsu.authorization_on_msu(username=passwords.auth_login, password=passwords.auth_pswd)

        print_section('Collecting users info')
        lmsu.scrap_data('users.csv')

        print_section(f'Collecting {len(lmsu.data)} user(s) achievements')
        lmsu.scrap_achievements()

    print_section(f'Filtering {len(lmsu.data)} user(s)')
    lmsu.filter_users()

    # Dump users data
    lmsu.dump()

    # Google table
    print_section('Connecting to Google Spreadsheets')
    worksheet = GSpread('key.json').get_worksheet()

    # Fill sheet
    print_section('Filling worksheet with our data')
    print_subsection('Filling header')
    cells = worksheet.range(range_grid((1, 1), (1, 5)))
    cells[0].value = 'ID'
    cells[1].value = 'ФИО'
    cells[2].value = 'Номер группы'
    cells[3].value = 'Баллы'
    cells[4].value = 'URL'
    worksheet.update_cells(cells)

    for i, (user_id, user) in enumerate(lmsu.data.items(), start=2):
        print_subsection(f'Filling user {user_id} data — {user["name"]}')
        cells = worksheet.range(range_grid((i, 1), (i, 5)))
        cells[0].value = user_id
        cells[1].value = user['name']
        cells[2].value = 'хз'
        cells[3].value = sum([int(x['score']) for x in user['achievements']])
        cells[4].value = f'http://lomonosov-msu.ru/rus/user/achievement/user/{user_id}/list'
        worksheet.update_cells(cells)
