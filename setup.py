#!/usr/bin/env python

import os, sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/machinetag.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
version = open("VERSION").read()
desc = open("README.md").read()

setup(
    name='machinetag',
    namespace_packages=['machinetag'],
    python_requires='>3',
    version=version,
    description='',
    author='Mapzen',
    url='https://github.com/whosonfirst/py-machinetag',
    packages=packages,
    scripts=[
    ],
    download_url='https://github.com/whosonfirst/py-machinetag/releases/tag/' + version,
    license='Perl Artistic')
