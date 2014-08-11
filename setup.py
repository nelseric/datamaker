#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='datamaker',
    version='0.0.1',
    packages = find_packages(),
    url='',
    license='',
    author='Eric Nelson',
    author_email='gauntletguy2@gmail.com',
    description='',
    entry_points = {
      'console_scripts': [
        'dm-import = datamaker.import:import_data',
        'dm-process = datamaker.input:do_input_stuff',
        'idle = idlelib.PyShell:main'
      ]
    }
)
