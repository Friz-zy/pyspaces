#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

""" 


import errno
from os import getpid
from os.path import exists
from .libc import libc, get_errno
from .args_aliases import na, get_all
from contextlib import contextmanager


@contextmanager
def setns(pid, proc='/proc', *args, **kwargs):
    """Change current namespaces to pid namespaces.

    Args:
      pid (str or int): pid of target process
      proc (str): root directory of proc fs,
        default is '/proc'
      *args (list): list of namespaces
      **kwargs (dict): dict of namespaces

    As args or kwargs expected one or many of keys:
    'all', 'ipc', 'newipc', 'mnt', 'newns',
    'net', 'newnet', 'pid', 'newpid',
    'user', 'newuser', 'uts', 'newuts'.
    In kwargs True or namespace file expected
    for each argument.
    If no one of them submitted 'all' will
    be used.

    """
    # all as default
    if ((len(args) == 0 and len(kwargs) == 0) or
       ('all' in args or 'all' in kwargs)):
        all_ns = True
    else:
        all_ns = False
    #'{proc}/{pid}/ns/{ns}'
    fdtmp = '{0}/{1}/ns/{2}'
    try:
        for ns in na:
            value = get_all(na[ns]['aliases'], args, kwargs, '')
            if all_ns or value:
                if exists(value):
                    namespace = value
                else:
                    namespace = fdtmp.format(proc, pid, na[ns]['aliases'][0])
                with open(namespace) as f:
                    if libc.setns(f.fileno(), na[ns]['flag']) == -1:
                        raise ValueError("Namespace file %s has invalid type %s" %
                                         (f.fileno(), na[ns]['flag'])
                        )
                break
        yield
    except:
        e = get_errno()
        raise OSError(e, errno.errorcode[e])
    finally:
        for ns in na:
            with open(fdtmp.format(proc, getpid(), na[ns]['aliases'][0])) as f:
                libc.setns(f.fileno(), na[ns]['flag'])
