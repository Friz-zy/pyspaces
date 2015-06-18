#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import os
import sys
from .setns import setns
from . import cloning as cl
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
          target (callable object): callable object to be
            invoked by the run() method
          args (tuple): argument tuple for the target
            invocation, default is ()
          kwargs (dict): dict of keyword arguments for
            the target invocation, default is {}
          all (bool): set all 6 namespaces,
            default is False
          newuts, uts (bool): set CLONE_NEWUTS flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
          newipc, ipc (bool): set CLONE_NEWIPC flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
          newuser, user (bool): set CLONE_NEWUSER flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
          newpid, pid (bool): set CLONE_NEWPID flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
          newnet, net (bool): set CLONE_NEWNET flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
          newns, mnt (bool): set CLONE_NEWNS flag if True,
            does not set flag enev with 'all' arg if False,
            default is None
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
          rootdir (str): path to new root, default is None
          workdir (str): path to new working dir,
            default is os.getcwd();
            if you set new rootdir, workdir
            path should be in new root tree
            and default will be '/'
          stdin (str, int, fd, fo): set new sys.stdin
            and 0 file descriptor,
            default '/dev/null' if daemonize
          stdout (str, int, fd, fo): set new sys.stdout
            and 1 file descriptor,
            default '/dev/null' if daemonize
          stderr (str, int, fd, fo): set new sys.stderr
            and 2 file descriptor,
            default '/dev/null' if daemonize
          daemonize (bool): execute target as
            daemon, default is False
          proc (str): root directory of proc fs,
            default is '/proc'
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
          flags (int): flags for clone, default is 0

        """
        self.args = args
        self.kwargs = kwargs
        self.kwargs['args'] = kwargs.get('args', ())
        self.kwargs['kwargs'] = kwargs.get('kwargs', {})

        self.clone_flags = kwargs.get('flags', 0)
        self.uid_map = pop('uid_map', args, kwargs, "")
        self.gid_map = pop('gid_map', args, kwargs, "")
        self.map_zero = pop('map_zero', args, kwargs, False)
        self.proc = kwargs.get('proc', '/proc')

        self.kwargs['proc'] = self.proc
        self.kwargs['rootdir'] = kwargs.get('rootdir', None)
        self.kwargs['workdir'] = kwargs.get('workdir', None)
        if self.kwargs['workdir'] in (None, False):
            if self.kwargs['rootdir']:
                self.kwargs['workdir'] = '/'
            else:
                self.kwargs['workdir'] = os.getcwd()
        self.kwargs['daemonize'] = pop('daemonize', args, kwargs, False)
        self.kwargs['stdin'] = kwargs.get('stdin', None)
        if self.kwargs['stdin'] in (None, False) and self.kwargs['daemonize']:
            self.kwargs['stdin'] = '/dev/null'
        self.kwargs['stdout'] = kwargs.get('stdout', None)
        if self.kwargs['stdout'] in (None, False) and self.kwargs['daemonize']:
            self.kwargs['stdout'] = '/dev/null'
        self.kwargs['stderr'] = kwargs.get('stderr', None)
        if self.kwargs['stderr'] in (None, False) and self.kwargs['daemonize']:
            self.kwargs['stderr'] = '/dev/null'

        # clear args and move all specific args to kwargs
        kwargs['all'] = pop('all', args, kwargs, False)

        for ns in na:
            value = pop_all(na[ns]['aliases'],
                            args, kwargs, None)
            if value is not None:
                kwargs[na[ns]['aliases'][0]] = value
            elif kwargs['all']:
                kwargs[na[ns]['aliases'][0]] = True
                value = True
            # set clone flags
            if value:
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

        Execution order:
          0.1) new ns and sigmask (Clone)
          0.2) set uid, gid (Clone)
          1) self.preup (mount, etc)
          4) self.daemonize
          5) self.chroot
          6) self.chdir
          7) self.chtty ?vagga before ns
          8) self.postup - in finally block
          9) self.exceptup - in except block
          10) self.preexec (networking, etc)
          11) execute self.target
          12) self.postexec - in finally block
          13) self.exceptexec - in except block

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

        TODO:
          apparmor
          selinux

        """
        try:
            self.preup()
            self.daemonize()
            self.chroot()
            self.chdir()
            self.chtty()
        except:
            self.exceptup()
            raise
        finally:
            self.postup()
        try:
            self.preexec()
            return_value = self.kwargs['target'](
                *self.kwargs['args'],
                **self.kwargs['kwargs']
            ) or 0
        except:
            self.exceptexec()
            raise
        finally:
            self.postexec()
        return return_value

    def preup(self):
        """Dummy function."""
        pass

    def daemonize(self):
        """Execute target as daemon

        Required:
          self.kwargs['daemonize'].

        """
        if self.kwargs['daemonize']:
            os.umask(0)
            os.setsid()
            pid = os.fork()
            if pid > 0:
                sys.exit(0)

    def chroot(self):
        """Change root with os.chroot.

        Change working directory to rootdir,
        then execute chroot and then again
        change working dir to workdir.

        Required:
          self.kwargs['rootdir']

        """
        if self.kwargs['rootdir']:
            os.chdir(self.kwargs['rootdir'])
            os.chroot(self.kwargs['rootdir'])

    def chdir(self):
        """Change working dir with os.chdir.

        Change current directory to new

        Required:
          self.kwargs['workdir']

        """
        if self.kwargs['workdir'] != os.getcwd():
            os.chdir(self.kwargs['workdir'])

    def chtty(self):
        """Change stdin, stdout, stderr.

        Required:
          self.kwargs['stdin']
          self.kwargs['stdout']
          self.kwargs['stderr']

        """
        stdin = self.kwargs['stdin']
        if stdin not in (None, False):
            if type(stdin) is str and os.path.exists(stdin):
                stdin = file(stdin, 'r')
                stdin = stdin.fileno()
            os.dup2(stdin, 0)
            os.dup2(stdin, sys.stdin.fileno())

        stdout = self.kwargs['stdout']
        if stdout not in (None, False):
            if type(stdout) is str and os.path.exists(stdout):
                stdout = file(stdout, 'r')
                stdout = stdout.fileno()
            os.dup2(stdout, 0)
            sys.stdout.flush()
            os.dup2(stdout, sys.stdout.fileno())

        stderr = self.kwargs['stderr']
        if stderr not in (None, False):
            if type(stderr) is str and os.path.exists(stderr):
                stderr = file(stderr, 'r')
                stderr = stderr.fileno()
            os.dup2(stderr, 0)
            sys.stderr.flush()
            os.dup2(stderr, sys.stderr.fileno())

    def postup(self):
        """Dummy function."""
        pass

    def exceptup(self):
        """Dummy function."""
        pass

    def preexec(self):
        """Dummy function."""
        pass

    def postexec(self):
        """Dummy function."""
        pass

    def exceptexec(self):
        """Dummy function."""
        pass

class Chroot(Container):
    """Class wrapper over `pyspaces.Container`

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
          "OSError [Errno 2] No such file or directory" error.
          You'd need all the other files the dynamic-linked
          program depends on, including shared libraries and
          any essential configuration/table/etc in the new
          root directories.
          [src](www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)

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
        ckwargs['rootdir'] = path
        ckwargs['target'] = target
        ckwargs['args'] = args
        ckwargs['kwargs'] = kwargs
        ckwargs['newuser'] = True
        ckwargs['newns'] = True
        Container.__init__(self, *cargs, **ckwargs)

class Inject(Process):
    """Class wrapper over `multiprocessing.Process`.

    Create process in namespaces of another one.

    The class is analagous to `threading.Thread`.

    """
    def __init__(self, target_pid, target, args=(), kwargs={}, proc='/proc', *pargs, **pkwargs):
        """Set new namespaces and execute Process.__init__

        Set self.setns as target with necessary args and kwargs.
        Then execute Process.__init__ with updated parameters.


        Args:
          target_pid (str or int): pid of target process,
            used for executing setns
          target (python function): python function
            for executing
          args (list): args for target,
            default is ()
          kwargs (dict): kwargs for target,
            default is {}
          proc (str): root directory of proc fs,
            default is '/proc'
          *pargs (list): arguments for Process.__init__
          **pkwargs (dict): arguments for Process.__init__

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
        if pop('all', pargs, pkwargs, False):
            nspaces.append('all')
        for ns in na:
            if pop_all(na[ns]['aliases'], pargs, pkwargs, None):
                nspaces.append(ns)

        pkwargs['args'] = ()
        pkwargs['kwargs'] = {
            'target_pid': target_pid, 'target': target,
            'args': args, 'kwargs': kwargs,
            'nspaces': nspaces, 'proc': proc,
        }
        pkwargs['target'] = self.setns
        Process.__init__(self, *pargs, **pkwargs)

    def setns(self, target_pid, target, args=(), kwargs={}, nspaces=[], proc='/proc'):
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
          all (bool): set all 6 namespaces,
            default is False
          newuts, uts (bool or str): enter uts namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None
          newipc, ipc (bool or str): enter ipc namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None
          newuser, user (bool or str): enter user namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None
          newpid, pid (bool or str): enter pid namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None
          newnet, net (bool or str): enter net namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None
          newns, mnt (bool or str): enter mount namespace,
            True or namespace file expected,
            does not enter ns enev with 'all' arg if False,
            default is None

        """
        with setns(target_pid, self.pid, proc, *nspaces):
            return target(*args, **kwargs)
