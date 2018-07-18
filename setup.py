#!/usr/bin/env python

from setuptools import setup

execfile('easy_tst/__version__.py')

setup(name='easy_tst',
      packages=['easy_tst'],
      version=__version__,
      description='tst automatically',
      author='Bruno Siqueira, Joao Espindula',
      author_email='bruno.siqueira@ccc.ufcg.edu.br',
      url='https://github.com/brobsc/easy_tst',
      download_url='https://github.com/brobsc/easy_tst/archive/{}.tar.gz'.format(__version__),
      install_requires=[
          'pyperclip',
          'requests',
      ],
      scripts=['bin/easy_tst'],
      )
