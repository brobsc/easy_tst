# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import subprocess
import json
import requests
import easy_helper
import logging


CACHE = {}
EXERCISES_DIR = 'exercicios_tst'

logger = logging.getLogger('easy_tst')

def checkout(exercise):
    code = exercise['checkout_name']
    logger.debug('Running "tst checkout {}"'.format(code))

    # Define the tst_root path in the function
    # FIXME: Move this to easy_helper (base_exercise_path)
    path = os.path.join(os.path.expanduser('~/'),
                        EXERCISES_DIR,
                        easy_helper.format_unit(exercise))
    logger.debug('Presumed path is {}'.format(path))

    # Create directory if it's not created already
    # FIXME: Directory creation belongs in easy_helper
    if not os.path.isdir(path):
        logger.debug('Path was invalid. Creating it'.format(path))
        os.makedirs(path)

    # Change directory to the path
    os.chdir(path)

    # Try to checkout
    tst_out = subprocess.check_output([
        'tst',
        'checkout',
        code
    ])

    logger.debug('"tst checkout" executed. Output was: {}'.format(tst_out))

    # Check checkout vality
    if 'token signature.' in tst_out:
        raise RuntimeError('Not logged in tst')
    if 'No object' in tst_out:
        raise ValueError('Invalid checkout code')

    result_path = os.path.join(path, code)
    logger.debug('Returning checkout path: {}'.format(result_path))

    return result_path


def get_exercises():
    logger.debug('Loading all exercises')
    # Return all exercises
    global CACHE
    result = CACHE or update_cache()
    logger.debug('Returning {} exercises'.format(len(result['assignments'])))
    return result['assignments']


def get_exercise_stats(code):
    logger.debug('Locating exercise with code "{}"'.format(code))
    exercises = get_exercises()

    # Try to get from current cached exercises first
    exercise = [e for e in exercises if e['checkout_name'] == code]

    if len(exercise) == 1:
        logger.debug('Exercise found on cache')
        return exercise[0]

    # If its not on cache, update current assignments
    logger.debug('Exercise not found on cache')
    exercises = update_cache()['assignments']

    exercise = [e for e in exercises if e['checkout_name'] == code][0]

    return exercise


def auth_key():
    logger.debug('Getting auth key')
    # Define path to the tst config.json file
    tst_path = os.path.expanduser('~/.tst/')
    logger.debug('Attempting to change dir into {}'.format(tst_path))
    os.chdir(tst_path)
    logger.debug('Changed dir to {}'.format(os.getcwd()))
    # Reads config.json file
    with open('config.json', 'r') as f:
        logger.debug('Loaded config.json successfully')
        config = json.load(f)

    # Return access code
    return config['access_token']


def request_to_tst():
    logger.debug('Sending request to tst api')
    # Requirements definition
    auth = auth_key()
    auth_header = {'Authorization': 'Bearer {}'.format(auth)}
    url = 'http://backend.tst-online.appspot.com/api'
    logger.debug('API url is {}'.format(url))

    # Request itself
    response = requests.get(url, headers=auth_header)

    return response


def update_cache():
    logger.debug('Cache update requested')
    response = request_to_tst()

    global CACHE

    if response.status_code == 400:
        logger.error('Response code was "400"')
        raise RuntimeError('Not logged in tst')

    CACHE = response.json()
    logger.debug('Cache has been updated')
    logger.debug('{} assignments on record'.format(len(CACHE['assignments'])))

    return CACHE


def main(code):
    logger.debug('Checkout on {} starting'.format(code))
    global CACHE

    if CACHE == {}:
        logger.debug('Cache is currently empty')

    exercise = get_exercise_stats(code)
    if len(exercise) == 0:
        raise IndexError
    code, label, name = exercise['checkout_name'], exercise['label'], exercise['name']

    logger.info('Checking out "{}": "{}"'.format(code, label))
    original_path = checkout(exercise)
    logger.debug('Getting desired path for "{}"'.format(code))
    destination_path = easy_helper.exercise_path(exercise)
    logger.debug('Requesting renaming from {} to {}'.format(original_path, destination_path))
    final_path = easy_helper.rename_directory(original_path, destination_path)

    student = {'name': CACHE['name'], 'email': CACHE['email']}
    logger.debug('Student generated. Current student is "{}: {}"'.format(student['name'], student['email']))

    logger.debug('Requesting file creation for "{}"'.format(code))
    easy_helper.create_exercise_file(name, final_path, exercise, student)

    logger.info('''Successful. Path is:
{}
'''.format(final_path))
