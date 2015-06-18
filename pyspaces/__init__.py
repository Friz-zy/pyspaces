#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


__description__ = 'Create process in linux namespaces'
__keywords__ = 'linux, container, namespaces'
__url__ = 'https://github.com/Friz-zy/pyspaces'
__author__ = 'Filipp Frizzy'
__credits__ = ["Filipp Frizzy"]
__license__ = "MIT"
__maintainer__ = "Filipp Frizzy"
__email__ = "filipp.s.frizzy@gmail.com"
__status__ = "Development"
__version__ = '1.4'

__all__ = ["cloning", "process", "libc", "cli", "setns", "args_aliases"]


from .process import Container, Chroot, Inject
from .setns import setns