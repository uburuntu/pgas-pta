from datetime import datetime

from pgas import passwords
from pgas.gspread_handle import GSpread
from pgas.lmsu_handle import LomonosovMSU
from pgas.utils import file_to_list, section


def main():
    #
    # Script arguments
    #
    lmsu_data_from_file = True
    achievements_fire_date_one_year = datetime(2018, 2, 14)
    achievements_fire_date_last_pgas = datetime(2018, 9, 14)
    users_filename = 'users.txt'
    users_last_pgas_filename = 'users_id_last_pgas.txt'
    google_key_filename = 'key.json'

    #
    # MSU
    #
    lmsu = LomonosovMSU()

    if lmsu_data_from_file:
        section('Loading data from file')
        lmsu.load('data_dump_old.json')
    else:
        section('Connecting to Lomonosov network')
        success = lmsu.authorization_on_msu(username=passwords.auth_login, password=passwords.auth_pswd)
        assert success

        section('Collecting users info')
        lmsu.scrap_data(users_filename)

        section(f'Collecting {len(lmsu.data)} user(s) achievements')
        lmsu.scrap_achievements()

    section(f'Filtering {len(lmsu.data)} user(s)')
    lmsu.delete_outdated_achievements(achievements_fire_date_one_year, achievements_fire_date_last_pgas,
                                      file_to_list(users_last_pgas_filename))

    section(f'Postprocess data')
    lmsu.data_postprocess()

    section(f'Dumping users data to file')
    lmsu.dump()

    section(f'Analyze extensions')
    lmsu.analyze_extensions()

    #
    # Google table
    #
    section('Connecting to Google Spreadsheets')
    gspread = GSpread(google_key_filename)

    section('Filling main worksheet with our data')
    gspread.fill_main_worksheet(lmsu.data)

    section('Filling achievements with our data')
    gspread.fill_achievements_worksheet(lmsu.data)

    section('The End!')


if __name__ == '__main__':
    main()
