import passwords
from gspread_handle import GSpread
from lmsu_handle import LomonosovMSU
from utils import print_section, print_subsection, range_grid

if __name__ == '__main__':
    # Script arguments
    lmsu_data_from_file = True
    users_filename = 'users.csv'
    google_key_filename = 'key.json'

    # MSU
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

    # Google table
    print_section('Connecting to Google Spreadsheets')
    gspread = GSpread(google_key_filename)

    # Fill main sheet
    worksheet = gspread.get_main_worksheet()

    print_section('Filling main worksheet with our data')
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

    # Fill achievements sheet
    worksheet = gspread.get_achievements_worksheet()

    print_section('Filling achievements with our data')
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
    worksheet.update_cells(cells)

    curr_line = 2
    for user_id, user in lmsu.data.items():
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
            worksheet.update_cells(cells)
            curr_line += 1
