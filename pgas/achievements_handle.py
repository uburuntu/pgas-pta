from enum import Enum

from pgas.utils import intersect_each_other


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
    def type_as_in_273_federal_law(type, score):
        types = AchievementsHandle.AchievementType
        subtypes = ['а', 'б', 'в'][type == types.education:]
        return types.type_273(type) + (subtypes[score % len(subtypes)] if type != types.unknown else '')

    @staticmethod
    def achievement_type(category) -> AchievementType:
        me = AchievementsHandle
        if category in me.education:
            return me.AchievementType.education
        if category in me.science:
            return me.AchievementType.science
        if category in me.social:
            return me.AchievementType.social
        if category in me.culture:
            return me.AchievementType.culture
        if category in me.sport:
            return me.AchievementType.sport

        print(f'\n[WARNING] Unknown achievement category: {category}')
        return me.AchievementType.unknown

    education = {
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
    }

    science = {
        'Грант',
        'Публикация в издании университетского уровня (относится к математике / физике / экономике, но издание не всеросссийского и не международного уровня)',
        'Публикация в издании всероссийского уровня (относится к относится к математике / физике / экономике, а издание из списка ВАК при Минобрнауки)',
        'Публикация в издании всероссийского уровня (относится к математике / физике / экономике, а издание из списка ВАК при Минобрнауки)',
        'Публикация в издании международного уровня (относится к математике / физике / экономике, а издание из баз Scopus или Springer)',
        'Публикация в издании международного уровня(относится к математике/физике/экономике, а издание из баз Scopus или Springer)',
        'Публикация иная (не относится к математике, физике или экономике)',
        'Награда на университетском уровне (в т.ч. за устное выступление с докладом)',
        'Награда на всероссийском уровне (в т.ч. за устное выступление с докладом)',
        'Награда на всероссийском уровне(в т.ч. за устное выступление с докладом)',
        'Награда на международном уровне (в т.ч. за устное выступление с докладом)',
        'Патент / свидетельство',
        'Наука (иное)',
        'Тезис в издании университетского уровня (относится к математике, физике или экономике, но не в издании всероссийского или международного уровня)',
        'Тезис в издании всероссийского уровня (относится к математике, физике или экономике и в издании из списка ВАК при Минобрнауки РФ (но не международного уровня))',
        'Тезис в издании международного уровня (относится к математике, физике или экономике и в издании из баз Scopus или Springer)'
    }

    social = {
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
        'Приемная комиссия(работа в часах)',
        'Конкурсовод',
        'Общественная деятельность (иное)',
        'Другое(не нашел подходящей категории)',
    }

    culture_by_degrees = [
        {
            'Диплом 3 степени факультетского уровня (культура)',
            'Диплом 2 степени факультетского уровня (культура)',
            'Диплом 1 степени факультетского уровня (культура)',
        },
        {
            'Членство в сборной университетского уровня (культура)',
            'Диплом 3 степени университетского уровня (культура)',
            'Диплом 2 степени университетского уровня (культура)',
            'Диплом 1 степени университетского уровня (культура)',
        },
        {
            'Членство в сборной городского уровня (культура)',
            'Диплом 3 степени городского уровня (культура)',
            'Диплом 2 степени городского уровня (культура)',
            'Диплом 1 степени городского уровня (культура)',
        },
        {
            'Членство в сборной регионального уровня (культура)',
            'Диплом 3 степени регионального уровня (культура)',
            'Диплом 2 степени регионального уровня (культура)',
            'Диплом 1 степени регионального уровня (культура)',
        },
        {
            'Членство в сборной межрегионального уровня (культура)',
            'Диплом 3 степени межрегионального уровня (культура)',
            'Диплом 2 степени межрегионального уровня (культура)',
            'Диплом 1 степени межрегионального уровня (культура)',
        },
        {
            'Членство в сборной всероссийского уровня (культура)',
            'Диплом 3 степени всероссийского уровня (культура)',
            'Диплом 2 степени всероссийского уровня (культура)',
            'Диплом 1 степени всероссийского уровня (культура)',
        },
        {
            'Членство в сборной международного уровня (культура)',
            'Диплом 3 степени международного уровня (культура)',
            'Диплом 2 степени международного уровня (культура)',
            'Диплом 1 степени международного уровня (культура)',
        },
    ]
    culture = set.union(*culture_by_degrees, {
        'Помощник организатора интеллектуальной игры',
        'Организатор интеллектуальной игры',
        'Организатор выступления на Дне Пифагора',
        'Участие в площадке Экспромта на Дне Мехмата / выступление на факультетском или университетском мероприятии',
        'Исполнитель главной роли на Дне Пифагора',
    })

    sport_by_degrees = [
        {
            'Диплом 3 степени факультетского уровня (спорт)',
            'Диплом 2 степени факультетского уровня (спорт)',
            'Диплом 1 степени факультетского уровня (спорт)',
        },
        {
            'Членство в сборной университетского уровня (спорт)',
            'Диплом 3 степени университетского уровня (спорт)',
            'Диплом 2 степени университетского уровня (спорт)',
            'Диплом 1 степени университетского уровня (спорт)',
        },
        {
            'Членство в сборной городского уровня (спорт)',
            'Диплом 3 степени городского уровня (спорт)',
            'Диплом 2 степени городского уровня (спорт)',
            'Диплом 1 степени городского уровня (спорт)',
        },
        {
            'Членство в сборной регионального уровня (спорт)',
            'Диплом 3 степени регионального уровня (спорт)',
            'Диплом 2 степени регионального уровня (спорт)',
            'Диплом 1 степени регионального уровня (спорт)',
        },
        {
            'Членство в сборной межрегионального уровня (спорт)',
            'Диплом 3 степени межрегионального уровня (спорт)',
            'Диплом 2 степени межрегионального уровня (спорт)',
            'Диплом 1 степени межрегионального уровня (спорт)',
        },
        {
            'Членство в сборной всероссийского уровня (спорт)',
            'Диплом 3 степени всероссийского уровня (спорт)',
            'Диплом 2 степени всероссийского уровня (спорт)',
            'Диплом 1 степени всероссийского уровня (спорт)',
        },
        {
            'Членство в сборной международного уровня (спорт)',
            'Диплом 3 степени международного уровня (спорт)',
            'Диплом 2 степени международного уровня (спорт)',
            'Диплом 1 степени международного уровня (спорт)',
        },
    ]
    sport = set.union(*sport_by_degrees)

    intersection = intersect_each_other(education, science, social, culture, sport)
    if len(intersection) != 0:
        print('\n[WARNING] Category intersection!')
        print(intersection)
