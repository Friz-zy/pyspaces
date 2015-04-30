#!/usr/bin/env python
# coding=utf-8 


__description__ = 'Create process in linux namespaces'
__keywords__ = 'linux, container, namespaces'
__url__ = 'https://github.com/Friz-zy/pyspaces'
__author__ = 'Filipp Frizzy'
__credits__ = ["Filipp Frizzy"]
__license__ = "MIT"
__maintainer__ = "Filipp Frizzy"
__email__ = "filipp.s.frizzy@gmail.com"
__status__ = "Development"
__version__ = '1.2.3'

__all__ = ["cloning", "process", "libc", "cli"]


from .process import Container, Chroot
