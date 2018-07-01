# coding: utf-8

from __future__ import print_function, unicode_literals

import os
import subprocess
import json
import requests
import easy_helper

from shutil import rmtree


CACHE = {}


def checkout(exercise, code):
    # Define the tst_root path in the function
    path = os.path.expanduser('~/') + 'exercicios-tst/' + easy_helper.format_unit(exercise) + '/'

    # Create directory if it's not created already
    if not os.path.isdir(path):
        os.makedirs(path)

    # Change directory to the path
    os.chdir(path)

    # Try to checkout
    tst_out = subprocess.check_output([
        'tst',
        'checkout',
        code
    ])

    # Check checkout vality
    if 'token signature.' in tst_out:
        raise RuntimeError('Not logged in tst.')
    if 'No object' in tst_out:
        raise ValueError('Invalid checkout code.')

    return path


def update_checkout(path, final_path, code):
    # FIXME: Erasing directory to update it. Currently a workaround.
    print('''
You already have a directory for this exercise with the following path:
{}
    
This directory will be erased and updated with the latest commit.'''.format(final_path))

    while True:
        decision = raw_input('Are you sure you want to proceed with this operation? (y/n) ').strip().lower()
        if decision == 'y':
            rmtree(final_path)
            os.rename(path + code, final_path)
            break
        elif decision == 'n':
            rmtree(path + code)
            break
        else:
            print('Please, just type "y" or "n"')
    print()


def get_exercise_stats(code, cache):
    # Try to get from response first
    if cache != {}:
        exercise = [e for e in cache['assignments'] if e['checkout_name'] == code]

        if len(exercise) == 1:
            return exercise[0]

    # If its not on cache, update current assignments
    cache = update_cache()

    exercise = [e for e in cache['assignments'] if e['checkout_name'] == code][0]

    return exercise


def auth_key():
    # Define path to the tst config.json file
    tst_path = os.path.expanduser('~/.tst/')
    os.chdir(tst_path)
    # Reads config.json file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Return access code
    return config['access_token']


def request_to_tst():
    # Requirements definition
    auth = auth_key()
    auth_header = {'Authorization': 'Bearer {}'.format(auth)}
    url = 'http://backend.tst-online.appspot.com/api'

    # Request itself
    response = requests.get(url, headers=auth_header)

    return response


def update_cache():
    response = request_to_tst()

    global CACHE

    if response.status_code == 400:
        raise RuntimeError('Not logged in tst.')

    CACHE = response.json()

    return CACHE


def main(code):

    global CACHE

    exercise = get_exercise_stats(code, CACHE)
    if len(exercise) == 0:
        raise IndexError
    code, label, name = exercise['checkout_name'], exercise['label'], exercise['name']

    print('Checking out "{}": "{}"'.format(code, label))
    original_path = checkout(exercise, code)
    final_path = easy_helper.rename_directory(original_path, exercise, code)

    student = {'name': CACHE['name'], 'email': CACHE['email']}

    easy_helper.create_exercise_file(name, final_path, exercise, student)

    print('''Successful. Path is:
{}
'''.format(final_path))
