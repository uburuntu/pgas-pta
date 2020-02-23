import asyncio
import json
import re
from collections import Counter
from datetime import datetime
from typing import Optional

import aiohttp
import math
from bs4 import BeautifulSoup

from pgas.achievements_handle import AchievementsHandle
from pgas.utils import subsection, is_non_zero_file


class LomonosovMSU:
    lmsu_url = 'https://lomonosov-msu.ru'

    def __init__(self, filename='lmsu_dump.json'):
        self.data = {}
        self.filename = filename

        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session is not None:
            await self.session.close()

    def dump_exist(self, filename: str = None):
        return is_non_zero_file(filename or self.filename)

    def load(self, filename: str = None):
        with open(filename or self.filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def dump(self, filename: str = None):
        with open(filename or self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=True, ensure_ascii=False)

    async def request(self, url, method='GET', data=None, headers=None):
        async with self.session.request(method, url, data=data, headers=headers) as response:
            return await response.read()

    async def authorization_on_msu(self, username, password):
        login_url = f'{self.lmsu_url}/rus/login'
        login_page = await self.request(login_url)
        csrf_token = BeautifulSoup(login_page, features='lxml').find('input', {'name': '_csrf_token'})['value']

        data = {'_username': username, '_password': password, '_remember_me': 'on', '_csrf_token': csrf_token}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        await self.request(f'{self.lmsu_url}/login_check', method='POST', data=data, headers=headers)

    async def scrap_user(self, user_id):
        response = await self.request(f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list')
        soup = BeautifulSoup(response, features="lxml")
        name_field = soup.find('h3', {'class': 'achievements-user__name'}) or \
                     soup.find('a', {'class': 'user-block__link user-block__link--logged'})
        user_data = {
            'name': name_field.text.strip(),
            'comment': '',
            'achievements': [],
        }
        subsection(f'Processing user \"{user_data["name"]}\"')
        for achievement in soup.find_all("article", {"class": "achievement"}):
            curr_data = {
                'title': achievement.find("a", {"class": "achievement__link"}).text.strip(),
                'category': achievement.find("p", {"class": "achievement__more"}).text.strip(),
                'score': int(achievement.find("span", {"class": "ach-pill"}).text),
                'checked': bool(achievement.find("input", {"checked": "checked"})),
                'url': self.lmsu_url + achievement.find("a", {"class": "achievement__link"})['href'],
                'date': '',
                'date_upload': '',
                'file': '',
                'comment': '',
                'comment_our': '',
            }
            user_data['achievements'].append(curr_data)
        return user_id, user_data

    async def scrap_users(self, users_id):
        coros = [self.scrap_user(user_id) for user_id in users_id]
        for coro in asyncio.as_completed(coros):
            user_id, self.data[user_id] = await coro

    async def scrap_achievement(self, achievement):
        response = await self.request(achievement['url'])
        soup = BeautifulSoup(response, features="lxml")
        for row in soup.find_all("div", {"class": "request__row"}):
            if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дата получения':
                achievement['date'] = row.find("div", {"class": "request__row-info"}).text.strip()
            if row.find("div", {"class": "request__row-title"}).text.strip() == 'Обращение от':
                achievement['date_upload'] = row.find("div", {"class": "request__row-info"}).text.strip()
            if row.find("div", {"class": "request__row-title"}).text.strip() == 'Дополнительно':
                achievement['comment'] = row.find("div", {"class": "request__row-info"}).text.strip()
        file = soup.find("a", {"class": "file-list__file-name"})
        achievement['file'] = self.lmsu_url + file.attrs['href'] if file else ''

    async def scrap_achievements(self):
        for user_id, user in self.data.items():
            subsection(f'Scrapping {len(user["achievements"]):>2} achievement(s) for \"{self.data[user_id]["name"]}\"')
            coros = [self.scrap_achievement(achievement) for achievement in user['achievements']]
            await asyncio.gather(*coros)
        subsection(f'Total achievements: {sum([len(user["achievements"]) for user in self.data.values()])}')

    def delete_outdated_achievements(self, date_one_year, date_last_pgas, ids_last_pgas):
        data = self.data
        for user_id, user in data.items():
            achievements = user['achievements']

            count_removed = 0
            for achievement in achievements[:]:
                date = datetime.strptime(achievement['date'], '%d.%m.%Y')
                date_upload = datetime.strptime(achievement['date_upload'], '%d.%m.%Y')
                if (date <= date_last_pgas and user_id in ids_last_pgas) or (date <= date_one_year):
                    achievements.remove(achievement)
                    count_removed += 1
                    if (date_upload > date_last_pgas and user_id in ids_last_pgas) or (
                            date_upload > date_one_year and user_id not in ids_last_pgas):
                        user['comment'] += f'— Дата достижения вне зачетного диапазона, дата обращения в зачетном диапазоне.\n'
            if count_removed > 0:
                subsection(f'Removed {count_removed:>2} achievements for \"{data[user_id]["name"]}\"')
        subsection(f'Total achievements left: {sum([len(user["achievements"]) for user in data.values()])}')

    @staticmethod
    def calculate_scores(achievements, score_with_unchecked):
        types = AchievementsHandle.AchievementType
        by_types = {e: [] for e in types}
        for achievement in achievements:
            if score_with_unchecked or achievement['checked']:
                by_types[AchievementsHandle.achievement_type(achievement['category'])].append(achievement)

        def calculate_two_top_degree(sets, achievements):
            scores_by_degrees = [0] * len(sets)
            score_other = 0
            for achievement in achievements:
                for i, set_ in enumerate(sets):
                    if achievement['category'] in set_:
                        scores_by_degrees[i] += achievement['score']
                        break
                else:
                    score_other += int(achievement['score'])
            return sum(sorted(scores_by_degrees, reverse=True)[:2]) + score_other

        return {
            types.unknown: sum([x['score'] for x in by_types[types.unknown]]),
            types.education: sum([x['score'] for x in by_types[types.education]]),
            types.science: sum([x['score'] for x in by_types[types.science]]),
            types.social: sum([x['score'] for x in by_types[types.social]]),
            types.culture: calculate_two_top_degree(AchievementsHandle.culture_by_degrees, by_types[types.culture]),
            types.sport: calculate_two_top_degree(AchievementsHandle.sport_by_degrees, by_types[types.sport]),
        }

    def calculate_score_and_type(self, achievements, score_with_unchecked):
        scores = self.calculate_scores(achievements, score_with_unchecked)
        sum_score, type = sum(scores.values()), max(scores, key=scores.get)
        return scores, sum_score, type.value, AchievementsHandle.type_as_in_273_federal_law(type, sum_score)

    def data_postprocess(self, score_with_unchecked=True):
        for user_id, user in self.data.items():
            user_name = user['name'].split()
            user['name'] = f'{user_name[2]} {user_name[0]} {user_name[1]}' if len(user_name) == 3 else f'{user_name[1]} {user_name[0]}'
            user['url'] = f'{self.lmsu_url}/rus/user/achievement/user/{user_id}/list'
            for achievement in user['achievements']:
                type = AchievementsHandle.achievement_type(achievement['category'])
                achievement['type'] = type.value
                if type == AchievementsHandle.AchievementType.sport or type == AchievementsHandle.AchievementType.culture:
                    if 'Диплом' in achievement['category']:
                        first_num = re.search(r'\d+', achievement['comment'])
                        if first_num:
                            first_num = int(first_num.group())
                            achievement['score_our'] = achievement['score'] * math.log10(first_num) if first_num > 10 else 1
                            achievement['comment_our'] += f'Количество участников: {first_num}.'
                        else:
                            achievement['comment_our'] += f'Warning! В комментарии отсутствует число участников.'
                            user['comment'] += f'— Проверить количество участников в соревнованиях.\n'
            user['score_by_types'], user['score'], user['type'], user['type_273'] = self.calculate_score_and_type(user['achievements'], score_with_unchecked)

    def analyze_extensions(self):
        extensions = []
        for user in self.data.values():
            for achievement in user['achievements']:
                extensions.append(achievement['file'].split('.')[-1])
        counter = Counter(extensions)
        subsection(counter.most_common())
