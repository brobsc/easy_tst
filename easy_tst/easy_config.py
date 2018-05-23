# coding: utf-8

import os
import json

CONFIG_PATH = os.path.expanduser('~/.easy_tst/')


def auth_key():
    tst_path = os.path.expanduser('~/.tst/')
    os.chdir(tst_path)
    with open('config.json', 'r') as f:
        config = json.load(f)

    return config['access_token']


def store(tst_root, name, mat, subdirs):
    if tst_root[-1] != '/':
        tst_root += '/'

    config = {
        'tst_root': tst_root,
        'name': name,
        'mat': mat,
        'subdirs': subdirs
    }

    if not os.path.isdir(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    os.chdir(CONFIG_PATH)

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ': '))


def load():
    conf = {}
    try:
        os.chdir(CONFIG_PATH)
        with open('config.json', 'r') as f:
            conf = (json.load(f))
    except OSError or IOError:
        # tst_wrapper tries to load config file on startup.
        # As CONFIG_PATH has not been created yet,
        # Dump a temp config file until wizard is ran for the first time
        if not os.path.isdir(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        os.chdir(CONFIG_PATH)
        config = {
            'tst_root': 'tst_test/',
            'name': 'Test',
            'mat': '000',
            'subdirs': 'y',
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4, separators=(',', ': '))
        with open('config.json', 'r') as f:
            conf = (json.load(f))
    finally:
        return conf
