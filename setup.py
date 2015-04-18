#!/usr/bin/env python
# coding=utf-8
from __future__ import with_statement
import sys
import pyspaces
from setuptools import setup, find_packages, Command
from os.path import join, dirname

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call(['py.test', '--cov', 'pyspaces', 'tests'])
        raise SystemExit(errno)

setup(
name='pyspaces',
version=pyspaces.__version__,
author = pyspaces.__author__,
author_email = pyspaces.__email__,
description = pyspaces.__description__,
license = pyspaces.__license__,
keywords = pyspaces.__keywords__,
url = pyspaces.__url__,
long_description=open(join(dirname(__file__), 'README.md')).read(),
packages=find_packages(),
cmdclass = {'test': PyTest},
tests_require=['pytest', 'pytest_capturelog', 'pytest-cov'],
install_requires=['click'],
entry_points={
'console_scripts': [
'space = pyspaces.cli:cli',
]
},
classifiers=[
'Development Status :: 3 - Alpha',
'Environment :: Console',
'Intended Audience :: Developers',
'Intended Audience :: System Administrators',
'License :: OSI Approved :: MIT License',
'Operating System :: POSIX :: Linux',
'Programming Language :: Python',
'Programming Language :: Python :: 2',
'Programming Language :: Python :: 3',
'Topic :: Software Development',
'Topic :: Software Development :: Build Tools',
'Topic :: Software Development :: Libraries',
'Topic :: Software Development :: Libraries :: Python Modules',
'Topic :: System :: Clustering',
'Topic :: System :: Systems Administration',
],
)