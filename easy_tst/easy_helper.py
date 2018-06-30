# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import shutil

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


def exercise_path(exercise):
    tst_exercises = tst_wrapper.EXERCISES_DIR
    return os.path.join(os.path.expanduser('~/'),
                        tst_exercises,
                        format_unit(exercise),
                        exercise['name'])


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


def rename_directory(base, destination):
    # Rename directory
    if not os.path.isdir(destination):
        shutil.move(base, destination)
    else:
        # FIXME: Erasing directory to update it. Currently a workaround.
        print('''
You already have a directory for this exercise with the following path:
{}

This directory will be erased and updated with the latest commit.'''.format(destination))

        while True:
            decision = raw_input('Are you sure you want to proceed with this operation? (y/n) ').strip().lower()
            if decision == 'y':
                shutil.rmtree(destination)
                shutil.move(base, destination)
                break
            elif decision == 'n':
                shutil.rmtree(base)
                break
            else:
                print('Please, just type "y" or "n"')
        print()

    return destination
