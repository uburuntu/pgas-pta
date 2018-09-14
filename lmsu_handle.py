from bs4 import BeautifulSoup
from datetime import datetime
from grab import Grab

from utils import csv_to_list, print_subsection


class LomonosovMSU:
    achievements_fire_day = datetime(2017, 9, 14)

    def __init__(self, username, password):
        self.grab = Grab()
        self.authorization_on_msu(username, password)

    def authorization_on_msu(self, username, password):
        self.grab.go('http://lomonosov-msu.ru/rus/login')
        self.grab.doc.set_input('_username', username)
        self.grab.doc.set_input('_password', password)
        self.grab.submit()

    def scrap_data(self, users_file_name):
        data = {}
        for user_id in csv_to_list(users_file_name):
            self.grab.go(f'http://lomonosov-msu.ru/rus/user/achievement/user/{user_id}/list')
            soup = BeautifulSoup(self.grab.doc.body, features="lxml")
            data[user_id] = {'name': soup.find('h3', {'class': 'achievements-user__name'}).text.strip(),
                             'achievements': []}
            print_subsection(f'Processing data for {user_id} — {data[user_id]["name"]}')
            for achievement in soup.find_all("article", {"class": "achievement"}):
                if achievement.find("input", {"checked": "checked"}):
                    curr_data = {
                        'title': achievement.find("a", {"class": "achievement__link"}).text.strip(),
                        'info': achievement.find("p", {"class": "achievement__more"}).text.strip(),
                        'score': achievement.find("span", {"class": "ach-pill"}).text,
                        'url': 'http://lomonosov-msu.ru' + achievement.find("a", {"class": "achievement__link"})['href']
                    }
                    data[user_id]['achievements'].append(curr_data)
        return data

    def scrap_achievements(self, data):
        for user_id, user in data.items():
            print_subsection(f'Processing {len(user["achievements"]):>2} achievement(s) for {user_id} '
                             f'— {data[user_id]["name"]}')
            for achievement in user['achievements']:
                self.grab.go(achievement['url'])
                soup = BeautifulSoup(self.grab.doc.body, features="lxml")
                for row in soup.find_all("div", {"class": "request__row"}):
                    if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дата получения':
                        achievement['date'] = row.find("div", {"class": "request__row-info"}).text.strip()
                        break

    def filter_users(self, data):
        for user_id, user in data.items():
            achievements = user['achievements']
            for achievement in achievements[:]:
                if datetime.strptime(achievement['date'], '%d.%m.%Y') < self.achievements_fire_day:
                    print_subsection(f'Excluding user ({user_id} — {data[user_id]["name"]}) achievement cause of date: '
                                     f'{achievement["date"]} ({achievement["url"]})')
                    achievements.remove(achievement)
