import asyncio
from datetime import datetime

from pgas import passwords
from pgas.gspread_handle import GSpread
from pgas.lmsu_handle import LomonosovMSU
from pgas.utils import section


async def main():
    #
    # Script arguments
    #
    date_one_year = datetime(2018, 6, 30)
    date_last_pgas = datetime(2019, 1, 31)

    google_spreadsheet_link = 'https://docs.google.com/spreadsheets/d/1Ay_o-48R0mCPBQGr1FLlp1gM_UVskanLViROAXG-LKc'
    google_key_filename = 'key.json'

    force_update_achievements = False
    count_score_with_unchecked_achievements = True

    #
    # MSU
    #
    lmsu = LomonosovMSU()
    gspread = GSpread(google_key_filename, google_spreadsheet_link)

    if lmsu.dump_exist() and not force_update_achievements:
        section('Loading data from file')
        lmsu.load()
    else:
        try:
            section('Connecting to Lomonosov network')
            await lmsu.authorization_on_msu(username=passwords.auth_login, password=passwords.auth_pswd)

            section('Collecting users info')
            await lmsu.scrap_users(gspread.get_ids())

            section(f'Collecting {len(lmsu.data)} user(s) achievements')
            await lmsu.scrap_achievements()
        finally:
            await lmsu.close()

    section(f'Filtering {len(lmsu.data)} user(s)')
    lmsu.delete_outdated_achievements(date_one_year, date_last_pgas, gspread.get_ids_last_pgas())

    section(f'Dumping users data to file')
    lmsu.dump()

    section(f'Postprocess data')
    lmsu.data_postprocess(count_score_with_unchecked_achievements)

    section(f'Analyze extensions')
    lmsu.analyze_extensions()

    #
    # Google table
    #
    section('Filling main worksheet with our data')
    gspread.fill_main_worksheet(lmsu.data)

    section('Filling achievements with our data')
    gspread.fill_achievements_worksheet(lmsu.data)

    section('The End!')


if __name__ == '__main__':
    # Init async loop
    ev_loop = asyncio.get_event_loop()
    try:
        # Run
        ev_loop.run_until_complete(main())

        # Wait for other tasks
        pending = asyncio.Task.all_tasks()
        ev_loop.run_until_complete(asyncio.gather(*pending))
    except KeyboardInterrupt:
        print('KeyboardInterrupt: good bye!')
    finally:
        ev_loop.run_until_complete(ev_loop.shutdown_asyncgens())
        ev_loop.close()
