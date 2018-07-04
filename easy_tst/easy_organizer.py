# coding: utf-8

from __future__ import print_function, unicode_literals

import tst_wrapper
import easy_helper

import os
import json
import sys
import logging


logger = logging.getLogger('easy_tst')

def clear_previous_line():
    sys.stdout.write("\033[F")  # Cursor up one line
    sys.stdout.write("\033[K")  # Clear to the end of line

def match_exercise(directory):
    logger.debug('Trying to mach {} into an exercise'.format(directory))
    exercises = tst_wrapper.get_exercises()
    dot_tst = os.path.join(directory, '.tst')
    os.chdir(dot_tst)
    logger.debug('Changed into "{}" directory'.format(dot_tst))
    iid = ''
    result = {}
    with open('tst.json', 'r') as f:
        logger.debug('tst.json loaded')
        tst_stats = json.load(f)
        # tst.json stores iid as an integer
        # but tst api returns a "key" as a string,
        # hence we convert to str early
        iid = str(tst_stats['iid'])
        logger.debug('iid was {}'.format(iid))

    for e in exercises:
        if e['key'] == iid:
            result = e

    return result


def organize(directory, ask=True):
    logger.debug('Organizing "{}"'.format(directory))
    logger.debug('Ask option is set to {}'.format(ask))
    exercise = match_exercise(directory)
    if exercise == {}:
        logger.debug('Could not find exercise for "{}"'.format(directory))
        return
    logger.debug('"{}" matches {}'.format(exercise['name']))

    destination = easy_helper.exercise_path(exercise)

    if directory == destination:
        logger.info('{} <- Already organized...'.format(directory))
        return

    logger.warning('{} -> {}'.format(directory, destination))

    if ask:
        answer = raw_input('Accept: ')

        if answer.lower() != 'y':
            clear_previous_line()
            clear_previous_line()
            logger.debug('Answer was invalid. {} skipped'.format(directory))
            return

        # Clear y answer
        clear_previous_line()

    logger.debug('Sending directory to renaming')
    easy_helper.rename_directory(directory, destination)


def get_tst_directories(path):
    result = []
    loading = ['-', '\\', '|', '/']
    current = 0

    for d, _, _ in os.walk(os.path.expanduser(path)):
        current_icon = loading[current % len(loading)]

        # End loading icon in carriage return. clear_previous_line bugs log output here
        print('[{}]'.format(current_icon), end='\r')

        if '.tst' in os.listdir(d):
            # Skip path if its home, since ~/.tst is tst's config dir
            if d == os.path.expanduser('~/'):
                continue
            logger.debug('"{}" is a tst folder'.format(d))
            result.append(d)
        current += 1

    logger.debug('Found tst {} folders. {} traversed'.format(len(result), current))

    return result


def main(ask, base_path):
    """Check for tst directories in OS"""
    logger.debug('organizer launched')
    logger.info('Looking for tst directories under {}'.format(os.path.expanduser(base_path)))
    directories = get_tst_directories(base_path)

    if ask:
        logger.warning('Press Y if you agree with the changes. Any other key to skip that folder.')

    for d in directories:
        organize(d, ask)

    logger.info('organize done!')


if __name__ == '__main__':
    main(True, '~/')
