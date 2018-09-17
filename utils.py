import csv

from gspread.utils import rowcol_to_a1


def range_grid(cell_start, cell_end):
    ''' range_grid((1,1),(3,3)) = A1:C3 '''
    return f'{rowcol_to_a1(*cell_start)}:{rowcol_to_a1(*cell_end)}'


def csv_to_list(file_name):
    with open(file_name, 'r') as file:
        reader_users = csv.reader(file)
        return set(x[0] for x in list(reader_users))


def print_section(text):
    me = print_section
    if not hasattr(me, 'count'):
        me.count = 1
    print('--- {:>4}. {}'.format(me.count, text))
    me.count += 1


def print_subsection(text):
    me = print_subsection
    parent = print_section
    if not hasattr(me, 'count'):
        me.count = 1
    if not hasattr(me, 'last') or me.last != getattr(parent, 'count', 0):
        me.count = 1
        me.last = getattr(parent, 'count', 0)
    print('----- {:>4}. {}'.format(me.count, text))
    me.count += 1
