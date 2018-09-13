import passwords
from gspread_handle import GSpread
from lmsu_handle import LomonosovMSU
from utils import range_grid

if __name__ == '__main__':
    # MSU
    lmsu = LomonosovMSU(username=passwords.auth_login, password=passwords.auth_pswd)
    data = lmsu.scrap_by_csv_with_users('users.csv')

    # Google table
    worksheet = GSpread('key.json').get_worksheet()

    # worksheet.acell('A1').value  # посомтреть что в ячейке
    # print(worksheet.cell(1, 2).value)  # тоже самое только по номеру (строка, столбец)
    # worksheet.add_rows(1)  # добавить строку
    # worksheet.update_acell('B1', 'Bingo!')
    # worksheet.update_cell(1, 2, 'Bingo!')

    # Change cells
    cell_list = worksheet.range(range_grid((1, 1), (3, 3)))
    print(cell_list)
    for cell in cell_list:
        cell.value = 'kek'

    # Update cells
    worksheet.update_cells(cell_list)
