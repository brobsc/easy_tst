# coding: utf-8

import os
import json

CONFIG_PATH = os.path.expanduser('~/.easy_tst/')

def auth_key():
    tst_path = os.path.expanduser('~/.tst/')
    os.chdir(tst_path)
    config = ''

    with open('config.json', 'r') as f:
        config = json.load(f)

    return config['access_token']


def store(tst_root, name, mat, subdirs):
    if tst_root[-1] != '/': tst_root += '/'

    config = {
        'tst_root': tst_root,
        'name': name,
        'mat': mat,
        'subdirs': subdirs
    }

    if not os.path.isdir(CONFIG_PATH): os.makedirs(CONFIG_PATH)
    os.chdir(CONFIG_PATH)

    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4, separators=(',', ': '))

def load():
    os.chdir(CONFIG_PATH)
    with open('config.json', 'r') as f:
        return (json.load(f))
