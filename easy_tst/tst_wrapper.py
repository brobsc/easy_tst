# coding: utf-8

from __future__ import print_function

import os
import sys
import subprocess
import requests
from unidecode import unidecode

import easy_config
# ALL PATHS MUST HAVE TRAILING SLASH

config = easy_config.load()


def header(label):
    result = '''# coding: utf-8
     
##{:44}##
# {:46} #
# {:44} #
# {:44} #
# {:44} #
# {:44} #
##{:44}##

'''.format( '#' * 44,
            'Disciplina: Programação 01 - 2018.1',
            'Nome: ' + config['name'],
            'Matrícula: ' + config['mat'],
            'Atividade: ' + label,
            'Unidade: ',
            '#' * 44
           )
    return result

# Takes a path and checkout a exercise on that path
def checkout(code, path):
    path = os.path.expanduser('~/') + config['tst_root']

    # Create directory if it's not created already
    if not os.path.isdir(path):
        os.makedirs(path)

    os.chdir(path)
    tst_out = subprocess.check_output([
        'tst',
        'checkout',
        code
    ])

    if 'token signature.' in tst_out:
        raise RuntimeError('Not logged in tst.')
    if 'No object' in tst_out:
        raise ValueError('Invalid checkout code.')

    # print('{}{}/'.format(path, code))
    return '{}{}/'.format(path, code)

def get_exercise_stats(code):
    auth = easy_config.auth_key()
    auth_header = { 'Authorization': 'Bearer {}'.format(auth) }
    url = 'http://backend.tst-online.appspot.com/api'

    r = requests.get(url, headers=auth_header)

    if r.status_code == 400: raise RuntimeError('Not logged in tst.')
    exercises = r.json()['assignments']
    exercise = [e for e in exercises if e['checkout_name'] == code][0]
    return exercise

# Remove accents and replace spaces with underscores
def format_filename(astr):
    result = astr.lower().replace(' ', '_')
    # https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    result = ''.join(e for e in result if e.isalnum() or e == '_')
    return unidecode(result)

# Create
def create_exercise_file(name, label, path):
    # Useless for now
    # name = format_filename(name)
    name += '.py'
    os.chdir(path)

    with open(name, 'a') as f:
        f.write(header(label))

    full_name = '{}{}'.format(path, name)

    # print(full_name)
    return full_name

# Receives a checkout `code`, a "raw" `name` and a base `path`
# cd to `path`
# tst checkout `code`
# cd to `code`
# appends HEADER to formated(`name`).py
# returns full file path ('/Users/me/tst/code1/my_exercise.py')
def full_checkout(code, path = 'tst/'):
    ex = get_exercise_stats(code)
    # Label has to be encoded because of utf-8 accents
    name, label = ex['name'], ex['label'].encode('utf-8')

    print('Checking out "{}": "{}"'.format(code, label))

    path = checkout(code, path)
    full_path = create_exercise_file(name, label, path)

    print('Checkout on {} done. Path is: {}'.format(code, full_path))
    return full_path

