# coding: utf-8

from __future__ import print_function, unicode_literals

import tst_wrapper
import easy_helper

import os
import json
import sys


def match_exercise(directory):
    exercises = tst_wrapper.get_exercises()
    os.chdir(directory + '/.tst')
    iid = ''
    result = {}
    with open('tst.json', 'r') as f:
        tst_stats = json.load(f)
        # tst.json stores iid as an integer
        # but tst api returns a "key" as a string,
        # hence we convert to str early
        iid = str(tst_stats['iid'])

    for e in exercises:
        if e['key'] == iid:
            result = e

    return result


def organize(directory, ask=True):
    exercise = match_exercise(directory)
    if exercise == {}:
        return

    destination = easy_helper.exercise_path(exercise)

    if directory == destination:
        print('{} <- Already organized...'.format(directory))
        return

    print('{} -> {}'.format(directory, destination))

    if ask:
        answer = raw_input('Accept: ')

        if answer.lower() != 'y':
            sys.stdout.write("\033[F")  # Cursor up one line
            sys.stdout.write("\033[K")  # Clear to the end of line
            sys.stdout.write("\033[F")  # Cursor up one line
            sys.stdout.write("\033[K")  # Clear to the end of line
            return

        # Clear y answer
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\033[K")  # Clear to the end of line

    easy_helper.rename_directory(directory, destination)


def get_tst_directories(path):
    result = []
    loading = ['-', '\\', '|', '/']
    current = 0
    for d, _, _ in os.walk(os.path.expanduser(path)):
        current_icon = loading[current % len(loading)]
        print('[{}]'.format(current_icon))
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\033[K")  # Clear to the end of line
        if '.tst' in os.listdir(d):
            # Skip path if its home, since ~/.tst is tst's config dir
            if d == os.path.expanduser('~/'):
                continue
            result.append(d)
        current += 1

    return result


def main(ask, base_path):
    """Check for tst directories in OS"""
    print('Looking for tst directories under {}'.format(os.path.expanduser(base_path)))
    directories = get_tst_directories(base_path)

    if ask:
        print('Press Y if you agree with the changes. Any other key to skip that folder.')

    for d in directories:
        organize(d, ask)


if __name__ == '__main__':
    main(True, '~/')
