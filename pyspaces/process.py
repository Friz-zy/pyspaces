#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


from .setns import setns
from . import cloning as cl
from inspect import getargspec
from multiprocessing import Process
from os import chroot, chdir, getcwd
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
          target (callable object): callable object to be
            invoked by the run() method
          args (tuple): argument tuple for the target
            invocation, default is ()
          kwargs (dict): dict of keyword arguments for
            the target invocation, default is {}
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
          target_pid (str or int): pid of target process,
            used for executing setns
          proc (str): root directory of proc fs,
            default is '/proc'
          rootdir (str): path to root, default is '/'
          workdir (str): path to working dir,
            default is os.getcwd();
            if you set new rootdir, workdir
            path should be in new root tree
          all (bool): set all 6 namespaces,
            default is False
          newuts (bool or str): set CLONE_NEWUTS flag,
            True or namespace file expected,
            default is False
          newipc (bool or str): set CLONE_NEWIPC flag,
            True or namespace file expected,
            default is False
          newuser (bool or str): set CLONE_NEWUSER flag,
            True or namespace file expected,
            default is False
          newpid (bool or str): set CLONE_NEWPID flag,
            True or namespace file expected,
            default is False
          newnet (bool or str): set CLONE_NEWNET flag,
            True or namespace file expected,
            default is False
          newns (bool or str): set CLONE_NEWNS flag,
            True or namespace file expected,
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
          io (bool): set CLONE_IO flag,
            default is False

        """
        self.args = args
        self.kwargs = kwargs
        self.kwargs['args'] = kwargs.get('args', ())
        self.kwargs['kwargs'] = kwargs.get('kwargs', {})

        # 1) clear args and move all to kwargs +
        # 2) change target to self.runup +
        # 3) functions for *id maps
        # 4) ns in (bool, file, fd)
        # 5) works with kwargs with get

        self.clone_flags = kwargs.get('flags', 0)
        self.uid_map = pop('uid_map', args, kwargs, "")
        self.gid_map = pop('gid_map', args, kwargs, "")
        self.map_zero = pop('map_zero', args, kwargs, False)
        self.proc = kwargs.get('proc', '/proc')

        self.kwargs['proc'] = self.proc
        self.kwargs['target_pid'] = kwargs.get('target_pid', 0)
        self.kwargs['rootdir'] = kwargs.get('rootdir', '/')
        self.kwargs['workdir'] = kwargs.get('workdir', getcwd())

        # clear args and move all specific args to kwargs
        value = pop('all', args, kwargs, False)
        if value:
            kwargs['all'] = value
            kwargs['newipc'] = kwargs.get('newipc', True)
            kwargs['newns'] = kwargs.get('newns', True)
            kwargs['newnet'] = kwargs.get('newnet', True)
            kwargs['newpid'] = kwargs.get('newpid', True)
            kwargs['newuser'] = kwargs.get('newuser', True)
            kwargs['newuts'] = kwargs.get('newuts', True)

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
        kwargs['target'] = self.runup
        kwargs['args'] = ()
        kwargs['kwargs'] = {}
        Process.__init__(self, *args, **kwargs)

    def runup(self):
        """Main wrapper over target function.

        TODO:
          0.1) [x] new ns and sigmask (Clone)
          0.2) [x] set uid, gid (Clone)
          1) [x] self.preup
          2) [ ] demonize
          2.1) [ ] change context - apparmor
          2.2) [ ] change context - selinux
          2.3) [x] self.nsenter
          2.5) [ ] self.chtty ?vagga before ns
          3) [x] self.chroot
          4) [x] self.chdir
          5) [x] self.networking
          6) [x] self.postup - in finally block
          7) [x] self.preexec
          8) [x] execute self.target
          9) [x] self.postexec - in finally block

        Required:
          self.kwargs['target']
          self.kwargs['args']
          self.kwargs['kwargs']

        Return:
          int: return of target function
            or 0 if no one exception was
            raised

        Raise:
          any exception

        """
        try:
            self.preup()
            self.nsenter()
            self.chtty()
            self.chroot()
            self.chdir()
            self.networking()
        finally:
            self.postup()
        try:
            self.preexec()
            return_value = self.kwargs['target'](
                *self.kwargs['args'],
                **self.kwargs['kwargs']
            ) or 0
        finally:
            self.postexec()
        return return_value

    def preup(self):
        """Dummy function."""
        pass

    def nsenter(self):
        """Change current namespaces to pid namespaces.

        Required:
          self.kwargs['target_pid']

        Uses:
          'all' or any of ns arguments
          self.proc

          """
        setns(**self.kwargs)

    def chtty(self):
        pass

    def chroot(self):
        """Change root with os.chroot.

        Change working directory to rootdir,
        then execute chroot and then again
        change working dir to workdir.

        Required:
          self.kwargs['rootdir']
          self.kwargs['workdir']

        """
        if self.kwargs['rootdir'] != '/':
            chdir(self.kwargs['rootdir'])
            chroot(self.kwargs['rootdir'])
            chdir(self.kwargs['workdir'])

    def chdir(self):
        """Change working dir with os.chdir.

        Change current directory to new

        Required:
          self.kwargs['workdir'].

        """
        if self.kwargs['workdir'] != getcwd():
            chdir(self.kwargs['workdir'])

    def networking(self):
        """Dummy function."""
        pass

    def postup(self):
        """Dummy function."""
        pass

    def preexec(self):
        """Dummy function."""
        pass

    def postexec(self):
        """Dummy function."""
        pass

class Chroot(Container):
    """Class wrapper over `pyspaces.Container`.

    Deprecated since 1.4! Use Container with rootdir,
    workdir, newuser and newns arguments.

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
            'rootdir': path, 'target': target,
            'workdir': ckwargs.get('workdir', path),
            'args': args, 'kwargs': kwargs
        }
        ckwargs['newuser'] = True
        ckwargs['newns'] = True
        Container.__init__(self, *cargs, **ckwargs)

class Inject(Container):
    """Class wrapper over `multiprocessing.Process`.

    Deprecated since 1.4! Use Container with target_pid
    argument.

    Create process in namespaces of another one.

    The class is analagous to `threading.Thread`.

    """
    def __init__(self, *pargs, **pkwargs):
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
        Container.__init__(self, *pargs, **pkwargs)
