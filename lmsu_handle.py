import json
from collections import Counter
from datetime import datetime

from bs4 import BeautifulSoup
from grab import Grab

from utils import AchievementsHandle, csv_to_list, subsection


class LomonosovMSU:
    lmsu_url = 'https://lomonosov-msu.ru'

    def __init__(self, achievements_fire_day):
        self.data = {}
        self.achievements_fire_day = achievements_fire_day
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
            subsection(f'Processing data for \"{data[user_id]["name"]}\"')
            for achievement in soup.find_all("article", {"class": "achievement"}):
                if achievement.find("input", {"checked": "checked"}):
                    curr_data = {
                        'title'   : achievement.find("a", {"class": "achievement__link"}).text.strip(),
                        'category': achievement.find("p", {"class": "achievement__more"}).text.strip(),
                        'score'   : achievement.find("span", {"class": "ach-pill"}).text,
                        'url'     : self.lmsu_url + achievement.find("a", {"class": "achievement__link"})['href']
                    }
                    data[user_id]['achievements'].append(curr_data)

    def scrap_achievements(self):
        data = self.data
        for user_id, user in data.items():
            subsection(f'Scrapping {len(user["achievements"]):>2} achievement(s) for \"{data[user_id]["name"]}\"')
            for achievement in user['achievements']:
                self.grab.go(achievement['url'])
                soup = BeautifulSoup(self.grab.doc.body, features="lxml")
                for row in soup.find_all("div", {"class": "request__row"}):
                    if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дата получения':
                        achievement['date'] = row.find("div", {"class": "request__row-info"}).text.strip()
                file = soup.find("a", {"class": "file-list__file-name"})
                achievement['file'] = self.lmsu_url + file.attrs['href'] if file else ''
        subsection(f'Total achievements: {sum([len(user["achievements"]) for user in data.values()])}')

    def filter_users(self):
        data = self.data
        for user_id, user in data.items():
            achievements = user['achievements']
            # Remove outdated achievements
            count_removed = 0
            for achievement in achievements[:]:
                if datetime.strptime(achievement['date'], '%d.%m.%Y') < self.achievements_fire_day:
                    achievements.remove(achievement)
                    count_removed += 1
            if count_removed > 0:
                subsection(f'Removed {count_removed:>2} achievements for \"{data[user_id]["name"]}\"')

            if False:
                # Left only 2 max achievements
                user['achievements'] = sorted(achievements, reverse=True, key=lambda x: int(x['score']))[:2]
        subsection(f'Total achievements left: {sum([len(user["achievements"]) for user in data.values()])}')

    def data_postprocess(self):
        data = self.data
        for user_id, user in data.items():
            user['url'] = f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list'
            for achievement in user['achievements']:
                achievement['type'] = AchievementsHandle.achievement_type(achievement['category'])
            user['type'] = AchievementsHandle.user_type(user['achievements'])
            user['score'] = sum([int(x['score']) for x in user['achievements']])

    def analyze_extensions(self):
        extensions = []
        for user in self.data.values():
            for achievement in user['achievements']:
                extensions.append(achievement['file'].split('.')[-1])
        counter = Counter(extensions)
        subsection(counter.most_common())
