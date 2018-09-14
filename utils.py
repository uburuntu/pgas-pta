import csv


def column_name(column):
    string = ''
    while column > 0:
        column, remainder = divmod(column - 1, 26)
        string = chr(65 + remainder) + string
    return string


def range_grid(cell_start, cell_end):
    ''' range_grid((1,1),(3,3)) = A1:C3 '''
    return f'{column_name(cell_start[1])}{cell_start[0]}:{column_name(cell_end[1])}{cell_end[0]}'


def csv_to_list(file_name):
    with open(file_name, 'r') as file:
        reader_users = csv.reader(file)
        return [x[0] for x in list(reader_users)]


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
