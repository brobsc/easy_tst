# coding: utf-8

from __future__ import print_function, unicode_literals

import easy_config
import os
import subprocess
import requests

from shutil import rmtree
from unidecode import unidecode


# ALL PATHS MUST HAVE TRAILING SLASH

config = easy_config.load_config()


# Takes a code and checkout a exercise and return path
def checkout(ex):
    code = ex['checkout_name']

    # Define the tst_root path in the function
    if config['subdirs'] == 'y':
        path = os.path.expanduser('~/') + config['tst_root'] + 'unidade' + get_unit(ex) + '/'
    else:
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
    if config['subdirs'] == 'y':  # Subdirs option YES
        # Get label, exercise number and returns path
        label = format_filename(ex['label'])  # Label has to be encoded because of utf-8 accents

        # Define final path
        final_path = '{}{}/'.format(path, label).encode('utf-8')

        # Rename directory
        if not os.path.isdir(final_path):
            os.rename(path + code, final_path)
        # FIXME: Erasing directory to update it. Currently a workaround.
        else:
            print('''
You already have a directory for this exercise with the following path:
{}

If you continue, this directory will be erased and replaced for a new one with files with the latest commit.'''.format(final_path))
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
        return final_path

    elif config['subdirs'] == 'n':  # Subdirs option NO
        return '{}{}/'.format(path, code)


# Creates a python file for the exercise
def create_exercise_file(ex, path):
    name, label = ex['name'], ex['label'].encode('utf-8')  # Label has to be encoded because of utf-8 accents

    # Add an extension to the file
    name += '.py'
    os.chdir(path)

    # Get the full name of the exercise and return it
    full_name = '{}{}'.format(path, name)

    # Writes the header in the file
    if is_zero_file(full_name):
        with open(name, 'a') as f:
            f.write(header(ex))

    return full_name


# Remove accents and replace spaces with underscores
def format_filename(astr):
    result = astr.lower().replace(' ', '_')
    # https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
    result = ''.join(e for e in result if e.isalnum() or e == '_')
    return unidecode(result)


# Do the checkout
def full_checkout(ex):
    label, code = ex['checkout_name'], ex['label']

    # Checkout and creates a python exercise file
    print('Checking out "{}": "{}"'.format(code, label))
    path = checkout(ex)
    full_path = create_exercise_file(ex, path)

    # Confirmation print and return full path of the exercise
    print('''Checkout on "{}" done. Path is:
{}'''.format(code, full_path))
    return full_path


# Gets by request an dictionary with information about the exercise
def get_exercise_stats(code, cached_response):
    # Try to get from response first
    exercise = [e for e in cached_response['assignments'] if e['checkout_name'] == code]

    if len(exercise) == 1:
        return exercise[0]

    # If its not on cache, update current assignements

    r = request_to_tst()

    # Check login in tst
    if r.status_code == 400:
        raise RuntimeError('Not logged in tst.')

    # Get the specific exercise and return it
    exercises = r.json()['assignments']
    exercise = [e for e in exercises if e['checkout_name'] == code][0]
    return exercise


# Get formatted unit from checkout code
def get_unit(ex):
    # Get raw unit from exercise
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
def header(ex):
    label = ex['label']
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
           'Nome: ' + config['name'],
           'Matrícula: ' + config['mat'],
           'Atividade: ' + label,
           'Unidade: ' + get_unit(ex),
           '#' * 44
           )
    # Encode is needed because of accents on Programação and Matrícula
    return result.encode('utf-8')


def request_to_tst():
    auth = easy_config.auth_key()
    auth_header = {'Authorization': 'Bearer {}'.format(auth)}
    url = 'http://backend.tst-online.appspot.com/api'

    # Request itself
    response = requests.get(url, headers=auth_header)

    return response


# Check if a file is empty
def is_zero_file(fpath):
    return not (os.path.isfile(fpath) and os.path.getsize(fpath) > 0)
