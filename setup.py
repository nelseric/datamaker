#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from Cython.Build import cythonize
import numpy
import sys

class PyTest(TestCommand):
  user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

  def initialize_options(self):
    TestCommand.initialize_options(self)
    self.pytest_args = []

  def finalize_options(self):
    TestCommand.finalize_options(self)
    self.test_args = []
    self.test_suite = True

  def run_tests(self):
    #import here, cause outside the eggs aren't loaded
    import pytest
    errno = pytest.main(self.pytest_args)
    sys.exit(errno)

setup(
  name='datamaker',
  version='0.0.1',
  packages=find_packages(),
  url='',
  license='',
  author='Eric Nelson',
  author_email='gauntletguy2@gmail.com',
  description='',
  ext_modules=cythonize("**/*.pyx"),
  include_dirs=[numpy.get_include()],
  tests_require=['pytest', 'pytest-cov'],
  cmdclass={'test': PyTest},

  entry_points={
    'console_scripts': [
      'dm-shell = datamaker.command.shell:shell',
      'dm-market-runner = datamaker.command.market_runner:run',
      'dm-import = datamaker.command.gen_ohlcv:gen_ohlcv',
      'dm-gen-training-data = datamaker.command.gen_training_data:gen_training_data',
      'dm-get-history = datamaker.command.get_historical:get_historical_data',
      'idle = idlelib.PyShell:main'
      ]
    }
)
