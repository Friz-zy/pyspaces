#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


from . import cloning as cl 
from collections import OrderedDict


# Careful the order is significant in this array.
# The user namespace comes first, so that it is entered
# first.  This gives an unprivileged user the potential to
# enter the other namespaces.
# via src of nsenter util
na = OrderedDict()
na['user'] = {
    'aliases': ['user', 'newuser'],
    'flag': cl.CLONE_NEWUSER
}
na['ipc'] = {
    'aliases': ['ipc', 'newipc'],
    'flag': cl.CLONE_NEWIPC
}
na['uts'] = {
    'aliases': ['uts', 'newuts'],
    'flag': cl.CLONE_NEWUTS
}
na['net'] = {
    'aliases': ['net', 'newnet'],
    'flag': cl.CLONE_NEWNET
}
na['pid'] = {
    'aliases': ['pid', 'newpid'],
    'flag': cl.CLONE_NEWPID
}
na['mnt'] = {
    'aliases': ['mnt', 'newns'],
    'flag': cl.CLONE_NEWNS
}

ca = {
    'vm': {
        'aliases': ['vm'],
        'flag': cl.CLONE_VM
    },
    'fs': {
        'aliases': ['fs'],
        'flag': cl.CLONE_FS
    },
    'files': {
        'aliases': ['files'],
        'flag': cl.CLONE_FILES
    },
    'sighand': {
        'aliases': ['sighand'],
        'flag': cl.CLONE_SIGHAND
    },
    'ptrace': {
        'aliases': ['ptrace'],
        'flag': cl.CLONE_PTRACE
    },
    'vfork': {
        'aliases': ['vfork'],
        'flag': cl.CLONE_VFORK
    },
    'parent': {
        'aliases': ['parent'],
        'flag': cl.CLONE_PARENT
    },
    'thread': {
        'aliases': ['thread'],
        'flag': cl.CLONE_THREAD
    },
    'sysvsem': {
        'aliases': ['sysvsem'],
        'flag': cl.CLONE_SYSVSEM
    },
    'settls': {
        'aliases': ['settls'],
        'flag': cl.CLONE_SETTLS
    },
    'settid': {
        'aliases': ['settid'],
        'flag': cl.CLONE_PARENT_SETTID
    },
    'child_cleartid': {
        'aliases': ['child_cleartid'],
        'flag': cl.CLONE_CHILD_CLEARTID
    },
    'detached': {
        'aliases': ['detached'],
        'flag': cl.CLONE_DETACHED
    },
    'untraced': {
        'aliases': ['untraced'],
        'flag': cl.CLONE_UNTRACED
    },
    'child_settid': {
        'aliases': ['child_settid'],
        'flag': cl.CLONE_CHILD_SETTID
    },
    'io': {
        'aliases': ['io'],
        'flag': cl.CLONE_IO
    },
}


def get(arg, args=(), kwargs={}, default=False):
    """Check if key in args or kwargs.

    If key is in args or kwargs,
    return its value or True,
    else return default.

    Args:
      arg (any): key for search
      args (list): list for search
      kwargs (dict): dict for search
      default (any): default value,
        default is False

    Return:
      Value if arg is key for kwargs
      True if arg in args
      default if arg not in args or kwargs

    """
    if arg in kwargs:
        return kwargs[arg]
    elif arg in args:
        return True
    return default

def get_all(aliases, args=(), kwargs={}, default=False):
    """Check if keys in args or kwargs.

    If keys is in args or kwargs,
    return its first exist alias value
    or True, else return default.

    Args:
      aliases (any iterable): keys for search
      args (list): list for search
      kwargs (dict): dict for search
      default (any): default value,
        default is False

    Return:
      Value if any key is key for kwargs
      True if any key in args
      default if arg not in args or kwargs

    """
    for arg in aliases:
        if arg in kwargs:
            return kwargs[arg]
        elif arg in args:
            return True
    return default

def pop(arg, args=(), kwargs={}, default=False):
    """Check if key in args or kwargs.

    If key is in args or kwargs, remove it
    and return its value or True,
    else return default.

    Args:
      arg (any): key for search
      args (list): list for search
      kwargs (dict): dict for search
      default (any): default value,
        default is False

    Return:
      Value if arg is key for kwargs
      True if arg in args
      default if arg not in args or kwargs

    """
    value = default
    if arg in args:
        value = True
        args.remove(arg)
    if arg in kwargs:
        value = kwargs[arg]
        del kwargs[arg]
    return value

def pop_all(aliases, args=(), kwargs={}, default=False):
    """Check if keys in args or kwargs.

    If keys is in args or kwargs, remove it
    and return its value or True,
    else return default.

    Args:
      aliases (any iterable): keys for search
      args (list): list for search
      kwargs (dict): dict for search
      default (any): default value,
        default is False

    Return:
      Value if any key is key for kwargs
      True if any key in args
      default if arg not in args or kwargs

    """
    value = default
    for arg in aliases:
        if arg in args:
            value = True
            args.remove(arg)
        if arg in kwargs:
            value = kwargs[arg]
            del kwargs[arg]
    return value