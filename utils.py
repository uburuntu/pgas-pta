import csv
from datetime import datetime
from enum import Enum
from operator import itemgetter

from gspread.utils import rowcol_to_a1


def range_grid(cell_start, cell_end):
    ''' range_grid((1,1),(3,3)) = A1:C3 '''
    return f'{rowcol_to_a1(*cell_start)}:{rowcol_to_a1(*cell_end)}'


def csv_to_list(file_name):
    with open(file_name, 'r') as file:
        reader_users = csv.reader(file)
        return sorted(set(x[0] for x in list(reader_users)))


def section(text):
    me = section
    if not hasattr(me, 'count'):
        me.count = 1
    if not hasattr(me, 'time'):
        me.time = datetime.now()
        print('--- {:>4}. {}'.format(me.count, text))
        return
    now = datetime.now()
    print('=== {:>4}. Section executed in {}\n'.format(me.count, now - me.time))
    me.time = now
    me.count += 1
    print('--- {:>4}. {}'.format(me.count, text))


def subsection(text):
    me = subsection
    parent = section
    if not hasattr(me, 'count'):
        me.count = 1
    if not hasattr(me, 'last') or me.last != getattr(parent, 'count', 0):
        me.count = 1
        me.last = getattr(parent, 'count', 0)
    print('----- {:>4}. {}'.format(me.count, text))
    me.count += 1


def intersect_each_other(*args):
    result = set()
    for i, i_set in enumerate(args):
        for j, j_set in enumerate(args):
            if i == j:
                continue
            result.update(i_set & j_set)
    return result


class AchievementsHandle:
    class AchievementType(Enum):
        unknown = 'Неизвестно'
        education = 'Учёба'
        science = 'Наука'
        social = 'Общественная деятельность'
        culture = 'Культура'
        sport = 'Спорт'

        @staticmethod
        def type_273(type):
            types = AchievementsHandle.AchievementType
            return {
                types.unknown  : 'n/a',
                types.education: '7',
                types.science  : '8',
                types.social   : '9',
                types.culture  : '10',
                types.sport    : '11',
            }[type]

    @staticmethod
    def user_type(achievements):
        def type_score(type):
            return sum([int(x['score']) if type == x['type'] else 0 for x in achievements])

        max_score = max([(x, type_score(x.value)) for x in AchievementsHandle.AchievementType], key=itemgetter(1))
        return max_score[0].value, AchievementsHandle.type_as_in_273_federal_law(*max_score)

    @staticmethod
    def type_as_in_273_federal_law(type, score):
        types = AchievementsHandle.AchievementType
        subtypes = ['а', 'б', 'в']
        return types.type_273(type) + (subtypes[type == types.education:][-score % 3] if type != types.unknown else '')

    @staticmethod
    def achievement_type(category):
        me = AchievementsHandle
        if category in me.education:
            return me.AchievementType.education.value
        if category in me.science:
            return me.AchievementType.science.value
        if category in me.social:
            return me.AchievementType.social.value
        if category in me.culture:
            return me.AchievementType.culture.value
        if category in me.sport:
            return me.AchievementType.sport.value

        print(f'[WARNING] Unknown achievement category: {category}')
        return me.AchievementType.unknown.value

    education = [
        'Диплом 3 степени за олимпиаду уровня 5',
        'Диплом 2 степени за олимпиаду уровня 5',
        'Диплом 1 степени за олимпиаду уровня 5',
        'Диплом 3 степени за олимпиаду уровня 4',
        'Диплом 2 степени за олимпиаду уровня 4',
        'Диплом 1 степени за олимпиаду уровня 4',
        'Диплом 3 степени за олимпиаду уровня 3',
        'Диплом 2 степени за олимпиаду уровня 3',
        'Диплом 1 степени за олимпиаду уровня 3',
        'Диплом 3 степени за олимпиаду уровня 2',
        'Диплом 2 степени за олимпиаду уровня 2',
        'Диплом 1 степени за олимпиаду уровня 2',
        'Диплом 3 степени за олимпиаду уровня 1',
        'Диплом 2 степени за олимпиаду уровня 1',
        'Диплом 1 степени за олимпиаду уровня 1',
    ]
    education = set(education)

    science = [
        'Грант',
        'Публикация в издании университетского уровня (относится к математике / физике / экономике, но издание не всеросссийского и не международного уровня)',
        'Публикация в издании всероссийского уровня (относится к относится к математике / физике / экономике, а издание из списка ВАК при Минобрнауки)',
        'Публикация в издании международного уровня (относится к математике / физике / экономике, а издание из баз Scopus или Springer)',
        'Публикация иная (не относится к математике, физике или экономике)',
        'Награда на университетском уровне (в т.ч. за устное выступление с докладом)',
        'Награда на всероссийском уровне (в т.ч. за устное выступление с докладом)',
        'Награда на международном уровне (в т.ч. за устное выступление с докладом)',
        'Патент / свидетельство',
        'Наука (иное)',
    ]
    science = set(science)

    social = [
        'Оформление локаций',
        'Оформление символики',
        'Помощник организатора среднего мероприятия (например, этап конкурса групп / чемпионат мехмата по гандболу / площадка на Фестивале Науки)',
        'Помощник организатора крупного мероприятия (например, день Мехмата или день Пифагора)',
        'Главный организатор малого мероприятия (например, открытый кубок мехмата по шахматам / брейнринг на мехмате)',
        'Главный организатор среднего мероприятия (например, этап конкурса групп)',
        'Главный организатор крупного мероприятия (например, день Мехмата или день Пифагора)',
        'Приемная комиссия: дежурный на весенней олимпиаде',
        'Приемная комиссия: координатор весенней олимпиады',
        'Проверка олимпиады 3 уровня (матпраздник и др. олимпиады для младших школьников)',
        'Проверка олимпиады 2 уровня (матем. многоборье и т.п.)',
        'Проверка олимпиады 1 уровня (рег. этап Всероссийской олимпиады, Московская математическая и т.п.)',
        'Семестр малого мехмата',
        'Куратор академической группы',
        'Летняя матшкола',
        'Приемная комиссия (работа в часах)',
        'Конкурсовод',
        'Общественная деятельность (иное)',
    ]
    social = set(social)

    culture = [
        'Членство в сборной университетского уровня (культура)',
        'Членство в сборной городского уровня (культура)',
        'Членство в сборной регионального уровня (культура)',
        'Членство в сборной межрегионального уровня (культура)',
        'Членство в сборной всероссийского уровня (культура)',
        'Членство в сборной международного уровня (культура)',
        'Диплом 3 степени факультетского уровня (культура)',
        'Диплом 2 степени факультетского уровня (культура)',
        'Диплом 1 степени факультетского уровня (культура)',
        'Диплом 3 степени университетского уровня (культура)',
        'Диплом 2 степени университетского уровня (культура)',
        'Диплом 1 степени университетского уровня (культура)',
        'Диплом 3 степени городского уровня (культура)',
        'Диплом 2 степени городского уровня (культура)',
        'Диплом 1 степени городского уровня (культура)',
        'Диплом 3 степени регионального уровня (культура)',
        'Диплом 2 степени регионального уровня (культура)',
        'Диплом 1 степени регионального уровня (культура)',
        'Диплом 3 степени межрегионального уровня (культура)',
        'Диплом 2 степени межрегионального уровня (культура)',
        'Диплом 1 степени межрегионального уровня (культура)',
        'Диплом 3 степени всероссийского уровня (культура)',
        'Диплом 2 степени всероссийского уровня (культура)',
        'Диплом 1 степени всероссийского уровня (культура)',
        'Диплом 3 степени международного уровня (культура)',
        'Диплом 2 степени международного уровня (культура)',
        'Диплом 1 степени международного уровня (культура)',
        'Помощник организатора интеллектуальной игры',
        'Организатор интеллектуальной игры',
        'Организатор выступления на Дне Пифагора',
        'Участие в площадке Экспромта на Дне Мехмата / выступление на факультетском или университетском мероприятии',
        'Исполнитель главной роли на Дне Пифагора',
    ]
    culture = set(culture)

    sport = [
        'Членство в сборной университетского уровня (спорт)',
        'Членство в сборной городского уровня (спорт)',
        'Членство в сборной регионального уровня (спорт)',
        'Членство в сборной межрегионального уровня (спорт)',
        'Членство в сборной всероссийского уровня (спорт)',
        'Членство в сборной международного уровня (спорт)',
        'Диплом 3 степени факультетского уровня (спорт)',
        'Диплом 2 степени факультетского уровня (спорт)',
        'Диплом 1 степени факультетского уровня (спорт)',
        'Диплом 3 степени университетского уровня (спорт)',
        'Диплом 2 степени университетского уровня (спорт)',
        'Диплом 1 степени университетского уровня (спорт)',
        'Диплом 3 степени городского уровня (спорт)',
        'Диплом 2 степени городского уровня (спорт)',
        'Диплом 1 степени городского уровня (спорт)',
        'Диплом 3 степени регионального уровня (спорт)',
        'Диплом 2 степени регионального уровня (спорт)',
        'Диплом 1 степени регионального уровня (спорт)',
        'Диплом 3 степени межрегионального уровня (спорт)',
        'Диплом 2 степени межрегионального уровня (спорт)',
        'Диплом 1 степени межрегионального уровня (спорт)',
        'Диплом 3 степени всероссийского уровня (спорт)',
        'Диплом 2 степени всероссийского уровня (спорт)',
        'Диплом 1 степени всероссийского уровня (спорт)',
        'Диплом 3 степени международного уровня (спорт)',
        'Диплом 2 степени международного уровня (спорт)',
        'Диплом 1 степени международного уровня (спорт)',
    ]
    sport = set(sport)

    intersection = intersect_each_other(education, science, social, culture, sport)
    if len(intersection) != 0:
        print('[WARNING] Category intersection!')
        print(intersection)
