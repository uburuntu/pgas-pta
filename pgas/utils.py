import os
from datetime import datetime

from gspread.utils import rowcol_to_a1


def is_non_zero_file(file_path):
    return os.path.isfile(file_path) and os.path.getsize(file_path) > 0


def range_grid(cell_start, cell_end):
    """ range_grid((1,1),(3,3)) = A1:C3 """
    return f'{rowcol_to_a1(*cell_start)}:{rowcol_to_a1(*cell_end)}'


def file_to_list(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        items = file.read().replace('\n', ' ').split()
        return items


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
