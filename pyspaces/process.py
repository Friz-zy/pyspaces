#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


from .setns import setns
from . import cloning as cl
from os import chroot, chdir
from inspect import getargspec
from multiprocessing import Process
from .args_aliases import na, ca, get, get_all, pop, pop_all


class Container(Process):
    """Class wrapper over `multiprocessing.Process`.

    Container objects represent activity that is run in a separate process.

    The class is analagous to `threading.Thread`.

    """
    _Popen = cl.Clone

    def __init__(self, *args, **kwargs):
        """Set clone flags and execute Process.__init__

        Args:
          *args (list): arguments for Process.__init__
          **kwargs (dict): arguments for Process.__init__
          flags (int): flags for clone, default is 0
          uid_map (bool, int, str, list): UID mapping
            for new namespace:
            bool: map current uid as root
            int: map given uid as root
            str: like int or in format
            ' '.join((<start uid in new ns>,
                      <start uid in current ns>,
                      <range to mapping>
            )). Example "0 1000 1" will map 1000 uid as root,
            "0 1000 1,1 1001 1" or "1000,1001"
            will map 1000 as root and 1001 as uid 1.
            list: list of int or str
            default is ""
          gid_map (bool, int, str, list): GID mapping
            for new namespace, format the same as uid_map,
            default is ""
          map_zero (bool): Map user's UID and GID to 0
            in user namespace, default is False
          all (bool): set all 6 namespaces,
            default is False
          vm (bool): set CLONE_VM flag,
            default is False
          fs (bool): set CLONE_FS flag,
            default is False
          files (bool): set CLONE_FILES flag,
            default is False
          sighand (bool): set CLONE_SIGHAND flag,
            default is False
          ptrace (bool): set CLONE_PTRACE flag,
            default is False
          vfork (bool): set CLONE_VFORK flag,
            default is False
          parent (bool): set CLONE_PARENT flag,
            default is False
          thread (bool): set CLONE_THREAD flag,
            default is False
          newns (bool): set CLONE_NEWNS flag,
            default is False
          sysvsem (bool): set CLONE_SYSVSEM flag,
            default is False
          settls (bool): set CLONE_SETTLS flag,
            default is False
          settid (bool): set CLONE_PARENT_SETTID flag,
            default is False
          child_cleartid (bool): set CLONE_CHILD_CLEARTID flag,
            default is False
          detached (bool): set CLONE_DETACHED flag,
            default is False
          untraced (bool): set CLONE_UNTRACED flag,
            default is False
          child_settid (bool): set CLONE_CHILD_SETTID flag,
            default is False
          newuts (bool): set CLONE_NEWUTS flag,
            default is False
          newipc (bool): set CLONE_NEWIPC flag,
            default is False
          newuser (bool): set CLONE_NEWUSER flag,
            default is False
          newpid (bool): set CLONE_NEWPID flag,
            default is False
          newnet (bool): set CLONE_NEWNET flag,
            default is False
          io (bool): set CLONE_IO flag,
            default is False

        """
        self.args = args
        self.kwargs = kwargs

        # 1) clear args and move all to kwargs +
        # 2) change target to self.runup +
        # 3) functions for *id maps
        # 4) ns in (bool, file, fd)
        # 5) works with kwargs with get

        self.clone_flags = get('flags', (), kwargs, 0)
        self.uid_map = pop('uid_map', args, kwargs, "")
        self.gid_map = pop('gid_map', args, kwargs, "")
        self.map_zero = pop('map_zero', args, kwargs, False)

        # clear args and move all specific args to kwargs
        value = pop('all', args, kwargs, False)
        if value:
            kwargs['all'] = value
            kwargs['newipc'] = True
            kwargs['newns'] = True
            kwargs['newnet'] = True
            kwargs['newpid'] = True
            kwargs['newuser'] = True
            kwargs['newuts'] = True

        for ns in na:
            value = pop_all(na[ns]['aliases'],
                            args, kwargs, False)
            if value:
                kwargs[na[ns]['aliases'][0]] = value
                # set clone flags
                self.clone_flags |= na[ns]['flag']

        for flag in ca:
            value = pop_all(ca[flag]['aliases'],
                            args, kwargs, False)
            if value:
                kwargs[ca[flag]['aliases'][0]] = value
                # set clone flags
                self.clone_flags |= ca[flag]['flag']

        kwargs = {}
        for k in getargspec(Process.__init__).args:
            if k in self.kwargs:
                kwargs[k] = self.kwargs[k]
        #kwargs['target'] = self.runup
        #kwargs['args'] = ()
        #kwargs['kwargs'] = {}
        Process.__init__(self, *args, **kwargs)

    def runup(self):
        """Main wrapper over target function.

        0) ns and sigmask
        1) preup
        2.1) change context: apparmor
        2.2) change context: selinux
        2.3) change context: nsenter
        3) std* ?vagga до ns
        4) chroot
        5) chdir
        6) setuid    ??
        7) networking
        8) postup
        9) preexec
        10) exec
        11) postexec

        https://github.com/coreos/rkt/blob/master/Documentation/devel/architecture.md
        https://github.com/coreos/rkt/blob/master/Documentation/devel/stage1-implementors-guide.md

        """
        pass

    def chroot(self):
        """Change root with os.chroot.

        Change current directory to chroot,
        then execute chroot and then again
        change current directory back.

        Requared self.chroot or
        self.kwargs['chroot'].

        """
        pass

    def chdir(self):
        """Change working dir with os.chdir.

        Change current directory to new

        Requared self.workdir or
        self.kwargs['workdir'].

        """
        pass

    def networking(self):
        """https://github.com/coreos/rkt/blob/master/Documentation/networking.md"""
        pass

    def nsenter(self):
        pass

    def preup(self):
        pass

    def postup(self):
        pass

    def preexec(self):
        pass

    def postexec(self):
        pass

class Chroot(Container):
    """Class wrapper over `pyspaces.Container`.

    Chroot objects represent activity that is run in a separate process
    in new filesystem and user namespaces.

    The class is analagous to `threading.Thread`.

    """
    def __init__(self, path, target, args=(), kwargs={}, *cargs, **ckwargs):
        """Set target and clone flags and execute Container.__init__

        Set newuser and newns clone flags, set self.chroot
        as target with necessary args and kwargs. Then
        execute Container.__init__ with updated parameters.

        Note:
          If the program you're trying to exec is dynamic
          linked, and the dynamic linker is not present in /lib
          in the chroot environment - you would get the
          "OSError: [Errno 2] No such file or directory" error.
          You'd need all the other files the dynamic-linked
          program depends on, including shared libraries and
          any essential configuration/table/etc in the new
          root directories.
          [src](http://www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)

        Args:
          path (str): path to chroot new root
          target (python function): python function
            for executing after chroot
          args (list): args for target,
            default is ()
          kwargs (dict): kwargs for target,
            default is {}
          *cargs (list): arguments for Container.__init__
          **ckwargs (dict): arguments for Container.__init__

        """
        ckwargs['args'] = ()
        ckwargs['kwargs'] = {
            'path': path, 'target': target,
            'args': args, 'kwargs': kwargs
        }
        ckwargs['target'] = self.chroot
        ckwargs['newuser'] = True
        ckwargs['newns'] = True
        Container.__init__(self, *cargs, **ckwargs)

    def chroot(self, path, target, args=(), kwargs={}):
        """Change root and execute target.

        Change root with os.chroot. Then execute
        target with args and kwargs.

        Args:
          path (str): path to chroot new root
          target (python function): python function
            for executing after chroot
          args (list): args for target,
            default is ()
          kwargs (dict): kwargs for target,
            default is {}

        """
        chroot(path)
        return target(*args, **kwargs)

class Inject(Container):
    """Class wrapper over `multiprocessing.Process`.

    Create process in namespaces of another one.

    The class is analagous to `threading.Thread`.

    """
    def __init__(self, target_pid, target, args=(), kwargs={}, proc='/proc', *pargs, **pkwargs):
        """Set new namespaces and execute Process.__init__

        Set self.setns as target with necessary args and kwargs.
        Then execute Process.__init__ with updated parameters.


        Args:
          target_pid (str or int): pid of target process
          target (python function): python function
            for executing
          args (list): args for target,
            default is ()
          kwargs (dict): kwargs for target,
            default is {}
          proc (str): root directory of proc fs,
            default is '/proc'
          *pargs (list): arguments for Container.__init__
          **pkwargs (dict): arguments for Container.__init__

        In args or kwargs expected one or many of
        many keys for setns:
        'all', 'ipc', 'newipc', 'mnt', 'newns',
        'net', 'newnet', 'pid', 'newpid',
        'user', 'newuser', 'uts', 'newuts'.
        If no one of them submitted 'all' will
        be used.

        """
        nspaces = []
        # all as default
        if 'all' in pargs or ('all' in pkwargs and pkwargs['all']):
            nspaces.append('all')
        for ns in na:
            for a in na[ns]['aliases']:
                if a in args or (a in pkwargs and pkwargs[a]):
                    nspaces.append(ns)

        pkwargs['args'] = ()
        pkwargs['kwargs'] = {
            'pid': target_pid, 'target': target,
            'args': args, 'kwargs': kwargs,
            'nspaces': nspaces, 'proc': proc,
        }
        pkwargs['target'] = self.setns
        Container.__init__(self, *pargs, **pkwargs)

    def setns(self, pid, target, args=(), kwargs={}, nspaces=[], proc='/proc'):
        """Change namespaces and execute target.

        Args:
          path (str): path to chroot new root
          target (python function): python function
            for executing after chroot
          args (list): args for target,
            default is ()
          kwargs (dict): kwargs for target,
            default is {}
          nspaces (list): list of namespaces for setns
          proc (str): root directory of proc fs,
            default is '/proc'

        """
        with setns(pid, proc, *nspaces):
            return target(*args, **kwargs)
