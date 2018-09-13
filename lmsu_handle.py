from bs4 import BeautifulSoup
from grab import Grab

from utils import csv_to_list


class LomonosovMSU:
    def __init__(self, username, password):
        self.grab = Grab()
        self.authorization_on_msu(username, password)

    def authorization_on_msu(self, username, password):
        self.grab.go('http://lomonosov-msu.ru/rus/login')
        self.grab.doc.set_input('_username', username)
        self.grab.doc.set_input('_password', password)
        self.grab.submit()

    def scrap_by_csv_with_users(self, users_file_name):
        data = {}
        for user in csv_to_list(users_file_name):
            self.grab.go('http://lomonosov-msu.ru/rus/user/profile/' + user)
            soup = BeautifulSoup(self.grab.doc.body, features="lxml")
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
