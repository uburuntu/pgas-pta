import json
from collections import Counter
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pgas.achievements_handle import AchievementsHandle
from pgas.utils import file_to_list, subsection


class LomonosovMSU:
    lmsu_url = 'https://lomonosov-msu.ru'

    def __init__(self):
        self.data = {}
        self.session = requests.session()

    def load(self, filename='data_dump.json'):
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def dump(self, filename='data_dump.json'):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=True, ensure_ascii=False)

    def authorization_on_msu(self, username, password):
        login_url = f'{self.lmsu_url}/rus/login'
        login_page = self.session.get(login_url)
        csrf_token = BeautifulSoup(login_page.text, features='lxml').find('input', {'name': '_csrf_token'})['value']

        data = {'_username': username, '_password': password, '_remember_me': 'on', '_csrf_token': csrf_token}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = self.session.post(f'{self.lmsu_url}/login_check', data=data, headers=headers, allow_redirects=False)
        # Success - if not redirect back to login
        return response.next.url != login_url

    def scrap_data(self, users_file_name):
        data = self.data
        for user_id in file_to_list(users_file_name):
            response = self.session.get(f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list')
            soup = BeautifulSoup(response.text, features="lxml")
            data[user_id] = {'name'        : soup.find('h3', {'class': 'achievements-user__name'}).text.strip(),
                             'achievements': []}
            subsection(f'Processing data for \"{data[user_id]["name"]}\"')
            for achievement in soup.find_all("article", {"class": "achievement"}):
                curr_data = {
                    'title'   : achievement.find("a", {"class": "achievement__link"}).text.strip(),
                    'category': achievement.find("p", {"class": "achievement__more"}).text.strip(),
                    'score'   : achievement.find("span", {"class": "ach-pill"}).text,
                    'checked' : bool(achievement.find("input", {"checked": "checked"})),
                    'url'     : self.lmsu_url + achievement.find("a", {"class": "achievement__link"})['href'],
                }
                data[user_id]['achievements'].append(curr_data)

    def scrap_achievements(self):
        data = self.data
        for user_id, user in data.items():
            subsection(f'Scrapping {len(user["achievements"]):>2} achievement(s) for \"{data[user_id]["name"]}\"')
            for achievement in user['achievements']:
                response = self.session.get(achievement['url'])
                soup = BeautifulSoup(response.text, features="lxml")
                for row in soup.find_all("div", {"class": "request__row"}):
                    if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дата получения':
                        achievement['date'] = row.find("div", {"class": "request__row-info"}).text.strip()
                file = soup.find("a", {"class": "file-list__file-name"})
                achievement['file'] = self.lmsu_url + file.attrs['href'] if file else ''
        subsection(f'Total achievements: {sum([len(user["achievements"]) for user in data.values()])}')

    def filter_users(self, achievements_fire_date_one_year, achievements_fire_date_last_pgas, users_id_last_pgas):
        data = self.data
        for user_id, user in data.items():
            achievements = user['achievements']

            # Remove outdated achievements
            count_removed = 0
            for achievement in achievements[:]:
                date = datetime.strptime(achievement['date'], '%d.%m.%Y')
                if (date < achievements_fire_date_last_pgas and user_id in users_id_last_pgas) or (date < achievements_fire_date_one_year):
                    achievements.remove(achievement)
                    count_removed += 1
            if count_removed > 0:
                subsection(f'Removed {count_removed:>2} achievements for \"{data[user_id]["name"]}\"')
        subsection(f'Total achievements left: {sum([len(user["achievements"]) for user in data.values()])}')

    def data_postprocess(self):
        data = self.data
        for user_id, user in data.items():
            user['url'] = f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list'
            for achievement in user['achievements']:
                achievement['type'] = AchievementsHandle.achievement_type(achievement['category'])
            user['type'], user['type_273'] = AchievementsHandle.user_type(user['achievements'])
            user['score'] = sum([int(x['score']) for x in user['achievements']])

    def analyze_extensions(self):
        extensions = []
        for user in self.data.values():
            for achievement in user['achievements']:
                extensions.append(achievement['file'].split('.')[-1])
        counter = Counter(extensions)
        subsection(counter.most_common())
