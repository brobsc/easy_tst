# coding: utf-8

from __future__ import print_function, unicode_literals

import easy_config
import os
import subprocess
import requests


from unidecode import unidecode


# ALL PATHS MUST HAVE TRAILING SLASH

config = easy_config.load_config()


# Takes a code and checkout a exercise and return path
def checkout(code):
    # Define the tst_root path in the function
    path = os.path.expanduser('~/') + config['tst_root']

    # Create directory if it's not created already
    if not os.path.isdir(path):
        os.makedirs(path)

    # Change directory to the path
    os.chdir(path)

    # Check if logged in tst and if the checkout code is valid
    tst_out = subprocess.check_output([
        'tst',
        'checkout',
        code
    ])
    if 'token signature.' in tst_out:
        raise RuntimeError('Not logged in tst.')
    if 'No object' in tst_out:
        raise ValueError('Invalid checkout code.')

    # Returns the path
    return '{}{}/'.format(path, code)


# Creates a python file for the exercise
def create_exercise_file(name, label, path, code):
    # Add an extension to the file
    name += '.py'
    os.chdir(path)

    # Writes the header in the file
    with open(name, 'a') as f:
        f.write(header(label, code))

    # Get the full name of the exercise and return it
    full_name = '{}{}'.format(path, name)
    return full_name


# Remove accents and replace spaces with underscores
def format_filename(astr):
    result = astr.lower().replace(' ', '_')
    # https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    result = ''.join(e for e in result if e.isalnum() or e == '_')
    return unidecode(result)


# Do the checkout
def full_checkout(code):
    # Gets info about the exercise
    ex = get_exercise_stats(code)
    name, label = ex['name'], ex['label'].encode('utf-8')  # Label has to be encoded because of utf-8 accents

    # Checkout and creates a python exercise file
    print('Checking out "{}": "{}"'.format(code, label))
    path = checkout(code)
    full_path = create_exercise_file(name, label, path, code)

    # Confirmation print and return full path of the exercise
    print('Checkout on {} done. Path is: {}'.format(code, full_path))
    return full_path


# Gets by request an dictionary with information about the exercise
def get_exercise_stats(code):
    # Information for the request
    auth = easy_config.auth_key()
    auth_header = {'Authorization': 'Bearer {}'.format(auth)}
    url = 'http://backend.tst-online.appspot.com/api'

    # Request itself
    r = requests.get(url, headers=auth_header)

    # Check login in tst
    if r.status_code == 400:
        raise RuntimeError('Not logged in tst.')

    # Get the specific exercise and return it
    exercises = r.json()['assignments']
    exercise = [e for e in exercises if e['checkout_name'] == code][0]
    return exercise


# Get formatted unit from checkout code
def get_unit(code):
    # Get raw unit from exercise
    ex = get_exercise_stats(code)
    unit_raw = ex['unit'].encode('utf-8')
    unit = ''

    # Get unit number from unit_raw
    for num in unit_raw:
        if num in '0123456789':
            unit += num
    # Format in two chars
    unit = unit.zfill(2)

    # Return unit from exercise
    return unit


# Defines a header in the exercise python file with info about the exercise
def header(label, code):
    result = '''# coding: utf-8

##{:44}##
# {:46} #
# {:44} #
# {:44} #
# {:44} #
# {:44} #
##{:44}##

'''.format('#' * 44,
           'Disciplina: Programação 01 - 2018.1',
           'Nome: ' + config['name'],
           'Matrícula: ' + config['mat'],
           'Atividade: ' + label,
           'Unidade: ' + get_unit(code),
           '#' * 44
           )
    # Encode is needed because of accents on Programação and Matrícula
    return result.encode('utf-8')


def is_logged_in():
    # FIXME: Duplicated code from get_exercise_stats
    # Information for the request
    auth = easy_config.auth_key()
    auth_header = {'Authorization': 'Bearer {}'.format(auth)}
    url = 'http://backend.tst-online.appspot.com/api'

    # Request itself
    r = requests.get(url, headers=auth_header)

    # Status code 400 means user is not logged in
    return r.status_code != 400
