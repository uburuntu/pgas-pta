from gspread_handle import GSpread
from utils import range_grid

if __name__ == '__main__':
    # MSU
    # lmsu = LomonosovMSU(username=passwords.auth_login, password=passwords.auth_pswd)
    # data = lmsu.scrap_data('users.csv')
    # data = lmsu.scrap_achievements(data)

    # Google table
    worksheet = GSpread('key.json').get_worksheet()

    # Fill sheet
    cells = worksheet.range(range_grid((1, 1), (1, 5)))
    cells[0].value = 'ID'
    cells[1].value = 'ФИО'
    cells[2].value = 'Номер группы'
    cells[3].value = 'Баллы'
    cells[4].value = 'URL'
    worksheet.update_cells(cells)

    for i, (user_id, user) in enumerate(data.items(), start=2):
        cells = worksheet.range(range_grid((i, 1), (i, 5)))
        cells[0].value = user_id
        cells[1].value = user['name']
        cells[2].value = 'хз'
        cells[3].value = sum([int(x['score']) for x in user['achievements']])
        cells[4].value = f'http://lomonosov-msu.ru/rus/user/profile/{user_id}'
        worksheet.update_cells(cells)
