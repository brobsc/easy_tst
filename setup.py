#!/usr/bin/env python

from setuptools import setup

setup(name='easy_tst',
      version='0.0.1',
      description='Easy Tst',
      author='N',
      author_email='n',
      url='',
      packages=['easy_tst'],
      install_requires=[
          'pyperclip',
          'requests',
          'unidecode',
      ],
      scripts=['bin/easy_tst'],
     )
