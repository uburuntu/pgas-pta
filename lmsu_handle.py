import json
from datetime import datetime

from bs4 import BeautifulSoup
from grab import Grab

from utils import csv_to_list, print_subsection, AchievementType


class LomonosovMSU:
    lmsu_url = 'https://lomonosov-msu.ru'
    achievements_fire_day = datetime(2017, 9, 14)

    def __init__(self):
        self.data = {}
        self.grab = None

    def load(self, filename='data_dump.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def dump(self, filename='data_dump.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=True, ensure_ascii=False)

    def authorization_on_msu(self, username, password):
        self.grab = Grab()
        self.grab.go(self.lmsu_url + '/rus/login')
        self.grab.doc.set_input('_username', username)
        self.grab.doc.set_input('_password', password)
        self.grab.submit()

    def scrap_data(self, users_file_name):
        data = self.data
        for user_id in csv_to_list(users_file_name):
            self.grab.go(f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list')
            soup = BeautifulSoup(self.grab.doc.body, features="lxml")
            data[user_id] = {'name'        : soup.find('h3', {'class': 'achievements-user__name'}).text.strip(),
                             'achievements': []}
            print_subsection(f'Processing data for {user_id} — {data[user_id]["name"]}')
            for achievement in soup.find_all("article", {"class": "achievement"}):
                if achievement.find("input", {"checked": "checked"}):
                    curr_data = {
                        'title'   : achievement.find("a", {"class": "achievement__link"}).text.strip(),
                        'category': achievement.find("p", {"class": "achievement__more"}).text.strip(),
                        'score'   : achievement.find("span", {"class": "ach-pill"}).text,
                        'url'     : self.lmsu_url + achievement.find("a", {"class": "achievement__link"})['href']
                    }
                    data[user_id]['achievements'].append(curr_data)

    def scrap_postprocess(self):
        data = self.data
        for user_id, user in data.items():
            user['url'] = f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list'
            for achievement in user['achievements']:
                achievement['type'] = AchievementType.achievement_type(achievement['category'])
            user['type'] = AchievementType.user_type(user['achievements'])

    def scrap_achievements(self):
        data = self.data
        for user_id, user in data.items():
            print_subsection(f'Processing {len(user["achievements"]):>2} achievement(s) for {user_id} '
                             f'— {data[user_id]["name"]}')
            for achievement in user['achievements']:
                self.grab.go(achievement['url'])
                soup = BeautifulSoup(self.grab.doc.body, features="lxml")
                for row in soup.find_all("div", {"class": "request__row"}):
                    if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дата получения':
                        achievement['date'] = row.find("div", {"class": "request__row-info"}).text.strip()
                file = soup.find("a", {"class": "file-list__file-name"})
                if file:
                    achievement['file'] = self.lmsu_url + file.attrs['href']

    def filter_users(self):
        data = self.data
        for user_id, user in data.items():
            achievements = user['achievements']
            # Remove outdated achievements
            for achievement in achievements[:]:
                if datetime.strptime(achievement['date'], '%d.%m.%Y') < self.achievements_fire_day:
                    print_subsection(f'Excluding user ({user_id} — {data[user_id]["name"]}) achievement cause of date: '
                                     f'{achievement["date"]} ({achievement["url"]})')
                    achievements.remove(achievement)

            if False:
                # Left only 2 max achievements
                user['achievements'] = sorted(achievements, reverse=True, key=lambda x: int(x['score']))[:2]
