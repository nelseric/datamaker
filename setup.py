#!/usr/bin/env python

from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='datamaker',
    version='0.0.1',
    packages = find_packages(),
    url='',
    license='',
    author='Eric Nelson',
    author_email='gauntletguy2@gmail.com',
    description='',
    ext_modules = cythonize("datamaker/c_process.pyx"),
    entry_points = {
      'console_scripts': [
        'dm-import = datamaker.import:import_data',
        'dm-shell = datamaker.process:shell',
        'dm-gen-output = datamaker.process:generate_outputs',
        'idle = idlelib.PyShell:main'
      ]
    }
)
