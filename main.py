import csv
import pprint

import gspread
from bs4 import BeautifulSoup
from grab import Grab
from oauth2client.service_account import ServiceAccountCredentials

import passwords


def csv_to_list(file_name):
    with open(file_name, 'r') as file:
        reader_users = csv.reader(file)
        return [x[0] for x in list(reader_users)]


def authorization_on_msu(grab, username=passwords.auth_login, password=passwords.auth_pswd):
    grab.go('http://lomonosov-msu.ru/rus/login')
    grab.doc.set_input('_username', username)
    grab.doc.set_input('_password', password)
    grab.submit()
    return grab


def authorization_on_google(file_key='key.json'):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(file_key, scope)
    return gspread.authorize(credentials)


def scrap_by_csv_with_users(grab, users_file_name):
    data = {}
    for user in csv_to_list(users_file_name):
        grab.go('http://lomonosov-msu.ru/rus/user/profile/' + user)
        soup = BeautifulSoup(grab.doc.body, features="lxml")
        data[user] = {'name'             : soup.find('h2', {'class': 'profile__title'}).text.strip(),
                      'true_achievements': []}
        for achievement in soup.find_all("article", {"class": "achievement"}):
            if achievement.find("input", {"checked": "checked"}):
                data[user]['true_achievements'].append(
                        {'name' : achievement.find("a", {"class": "achievement__link"}).text.strip(),
                         'info' : achievement.find("p", {"class": "achievement__more"}).text.strip(),
                         'score': achievement.find("span", {"class": "ach-pill"}).text,
                         'url'  : achievement.find("a", {"class": "achievement__link"})['href']})
            else:
                pass
                # pprint.pprint(data[user])
    return data


def range_grid(cell_start, cell_end):
    ''' range_grid((1,1),(3,3)) = A1:C3 '''
    start_row, start_col = cell_start[0], cell_start[1]
    end_row, end_col = cell_end[0], cell_end[1]
    cell_range = '{col_i}{row_i}:{col_f}{row_f}'.format(
            col_i=chr((start_col - 1) + ord('A')),  # converts number to letter
            col_f=chr((end_col - 1) + ord('A')),  # subtract 1 because of 0-indexing
            row_i=start_row,
            row_f=end_row)
    return cell_range


if __name__ == '__main__':
    # MSU
    g = Grab()
    g = authorization_on_msu(g)
    data = scrap_by_csv_with_users(grab=g, users_file_name='users.csv')
    pprint.pprint(data)

    # Google table
    gc = authorization_on_google()
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc')

    if False:
        # Выдать доступ указанному пользователю
        sh.share('gmail@gmail.com', perm_type='user', role='writer')

        # sh = gc.create('Spreadsheet') # в начале 1000 строк, сами не добавляются при обращении, поэтому приходится добавлять вручную
    # print(sh) # тут можно взять ссылку на документ  |  https://docs.google.com/spreadsheets/ + ...
    worksheet = sh.get_worksheet(0)  # взять лист по номеру

    # worksheet.acell('A1').value  # посомтреть что в ячейке
    # print(worksheet.cell(1, 2).value)  # тоже самое только по номеру (строка, столбец)
    # worksheet.add_rows(1)  # добавить строку
    # worksheet.update_acell('B1', 'Bingo!')
    # worksheet.update_cell(1, 2, 'Bingo!')

    cell_list = worksheet.range(range_grid((1, 1), (3, 3)))
    print(cell_list)
    for cell in cell_list:
        cell.value = 'kek'

    # Update in batch
    worksheet.update_cells(cell_list)
