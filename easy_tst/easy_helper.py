# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import tst_wrapper


def create_exercise_file(name, path, exercise, student):
    # Add an extension to the file
    python_file = name + '.py'
    os.chdir(path)

    # Get the full name of the exercise and return it
    path_python_file = '{}{}'.format(path, python_file)

    # Writes the header in the file
    if is_zero_file(path_python_file):
        with open(python_file, 'a') as f:
            f.write(header(exercise, student))


def format_unit(exercise):
    # Get raw unit from exercise
    unit_raw = exercise['unit'].encode('utf-8')
    unit = ''

    # Get unit number from unit_raw
    for char in unit_raw:
        if char.isdigit():
            unit += char
    # Format in two chars
    unit = 'unidade' + unit.zfill(2)

    # Return unit from exercise
    return unit


def header(exercise, student):
    result = '''# coding: utf-8

##{:44}##
# {:44} #
# {:44} #
# {:44} #
# {:44} #
# {:44} #
##{:44}##


'''.format('#' * 44,
           'Disciplina: Programação 01 - 2018.1',
           'Nome: ' + student['name'],
           'E-mail: ' + student['email'],
           'Atividade: ' + exercise['label'],
           'Unidade: ' + format_unit(exercise)[-2::],
           '#' * 44
           )

    # Encode is needed because of accents on Programação
    return result.encode('utf-8')


def is_zero_file(fpath):
    return not (os.path.isfile(fpath) and os.path.getsize(fpath) > 0)


def is_logged_in():
    r = tst_wrapper.request_to_tst()

    logged_in = (r.status_code != 400)

    if not logged_in:
        print('Please log on tst (Run tst login).')
        raise RuntimeError('Not logged in tst.')


def rename_directory(path, exercise, code):
    # Define final path
    final_path = '{}{}/'.format(path, exercise['name'])

    # Rename directory
    if not os.path.isdir(final_path):
        os.rename(path + code, final_path)
    else:
        tst_wrapper.update_checkout(path, final_path, code)

    return final_path
