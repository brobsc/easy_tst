# coding: utf-8

from __future__ import print_function, unicode_literals

import json
import os


# Define the configuration path of easy_tst
CONFIG_PATH = os.path.expanduser('~/.easy_tst/')


# Get the auth key of the user
def auth_key():
    # Define path to the tst config.json file
    tst_path = os.path.expanduser('~/.tst/')
    os.chdir(tst_path)
    # Reads config.json file
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Return access code
    return config['access_token']


# Collect settings data from the user
def config_wizard():
    while True:
        # Define user Name
        config = load_config()

        print('''- Current Settings:
Name: {}
Root: {}
Mat: {}
Subdirs: {} 

Input your desired configuration. To maintain current settings use "---" as input.'''.format(config['name'],
                                                                                             config['tst_root'],
                                                                                             config['mat'],
                                                                                             config['subdirs']))

        name = raw_input('Name: ').decode('utf-8')
        if name == '---':
            name = config['name']

        # Define Root dir
        tst_root = raw_input('Root: ').decode('utf-8')
        if tst_root == '---':
            tst_root = config['tst_root']
        elif tst_root[-1] != '/':
            tst_root += '/'

        # Define user ID
        mat = raw_input('Mat: ').decode('utf-8')
        if mat == '---':
            mat = config['mat']

        # Define subdirs preference
        while True:
            sub = raw_input('Subdirs? (y/n) ').lower().decode('utf-8')
            if sub == '---':
                sub = config['subdirs']
                break
            elif sub != 'y' and sub != 'n':
                print('Entered value different than Y and N')
                print('Type just Y or N')
            else:
                break

        print('''
- Input Settings:
Name: {}
Root: {}
Mat: {}
Subdirs: {}'''.format(name, tst_root, mat, sub))

        while True:
            decision = raw_input('Do you want to store these settings? (y/n) ').lower().decode('utf-8')
            if decision == 'y':
                break
            elif decision == 'n':
                break
            else:
                print('Entered value different than Y and N')
                print('Type just Y or N')

        if decision == 'y':
            break
        else:
            print('''Ok! Input your data again.
            ''')
    config = {
        'tst_root': tst_root,
        'name': name,
        'mat': mat,
        'subdirs': sub
    }

    store_config(config)


def load_config():
    conf = {}
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    os.chdir(CONFIG_PATH)

    try:
        os.chdir(CONFIG_PATH)
        with open('config.json', 'r') as f:
            conf = (json.load(f))
    except IOError or OSError:
        reset_config()
        with open('config.json', 'r') as f:
            conf = (json.load(f))
    finally:
        return conf


def store_config(config):
    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    os.chdir(CONFIG_PATH)

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ': '))


def reset_config():
    config = {
        'tst_root': 'tst_test/',
        'name': 'Test',
        'mat': '000',
        'subdirs': 'y',
    }

    store_config(config)
