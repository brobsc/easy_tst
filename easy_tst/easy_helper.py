# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import shutil
import logging
import errno

import tst_wrapper

logger = logging.getLogger('easy_tst')

def dot_easy_tst():
    # Better way taken from: https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    # Create ~/.easy_tst
    dot_easy_tst = os.path.expanduser(os.path.join('~', '.easy_tst'))
    try:
        os.makedirs(dot_easy_tst)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(dot_easy_tst):
            pass
        else:
            raise

    return dot_easy_tst


def create_exercise_file(name, path, exercise, student):
    logger.debug('Creating file for "{}"'.format(name))
    # Add an extension to the file
    python_file = name + '.py'
    os.chdir(path)

    # Get the full name of the exercise and return it
    path_python_file = os.path.join(path, python_file)
    logger.debug('Full path is {}'.format(path_python_file))

    # Writes the header in the file
    if is_zero_file(path_python_file):
        logger.debug('File is empty')
        with open(python_file, 'a') as f:
            f.write(header(exercise, student))

    logger.debug('{} created'.format(path_python_file))


def exercise_path(exercise):
    logger.debug('Generating desired path for {}'.format(exercise['name']))
    tst_exercises = tst_wrapper.EXERCISES_DIR
    result = os.path.join(os.path.expanduser('~/'),
                        tst_exercises,
                        format_unit(exercise),
                        exercise['name'])
    logger.debug('Desired path is {}'.format(result))

    return result


def format_unit(exercise):
    logger.debug('Formatting unit for {}'.format(exercise['name']))

    # Get raw unit from exercise
    unit_raw = exercise['unit'].encode('utf-8')
    logger.debug('Unit is {}'.format(unit_raw))
    unit = ''

    # Get unit number from unit_raw
    for char in unit_raw:
        if char.isdigit():
            unit += char
    # Format in two chars
    unit = 'unidade' + unit.zfill(2)

    # Return unit from exercise
    logger.debug('Resulting unit is {}'.format(unit))
    return unit


def header(exercise, student):
    logger.debug('Generating header for {}'.format(exercise['name']))
    logger.debug('Received "{}: {}" as student'.format(student['name'], student['email']))
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
    logger.debug('Header done')
    return result.encode('utf-8')


def is_zero_file(fpath):
    logger.debug('Checking if {} is empty'.format(fpath))
    return not (os.path.isfile(fpath) and os.path.getsize(fpath) > 0)


def is_logged_in():
    logger.debug('Checking login status')
    r = tst_wrapper.request_to_tst()
    logger.debug('Request status code is "{}"'.format(r.status_code))

    logged_in = (r.status_code != 400)

    if not logged_in:
        logger.info('Please log on tst (Run tst login)')
        logger.error('Not logged in tst')
        raise RuntimeError('Not logged in tst')


def rename_directory(base, destination):
    logger.debug('Renaming {} to {}'.format(base, destination))
    # Rename directory
    if not os.path.isdir(destination):
        logger.debug('{} was empty. Moving {} to it'.format(destination, base))
        shutil.move(base, destination)
    else:
        # FIXME: Erasing directory to update it. Currently a workaround.
        logger.warning('''
You already have a directory for this exercise with the following path:
{}

This directory will be ERASED and updated with the latest commit'''.format(destination))

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
                logger.warning('Please, just type "y" or "n"')
        logger.info('')

    logger.debug('{} renamed to {} succesfully'.format(base, destination))
    return destination
