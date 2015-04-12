#!/usr/bin/env python
# coding=utf-8


from .cloning import *
from multiprocessing import Process


class Container(Process):
    """Class wrapper over `multiprocessing.Process`.

    Container objects represent activity that is run in a separate process.

    The class is analagous to `threading.Thread`.

    """
    _Popen = Clone

    def __init__(self, *args, **kwargs):
        """Set clone flags and execute Process.__init__

        Args:
          *args (list): arguments for Process.__init__
          **kwargs (dict): arguments for Process.__init__
          flags (int): flags for clone, default is 0
          uid_map (str): UID mapping for new namespace,
            default is ""
          gid_map (str): GID mapping for new namespace,
            default is ""
          map_zero (bool): Map user's UID and GID to 0
            in user namespace, default is False
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
        self.clone_flags = kwargs.pop('flags', 0)
        self.uid_map = kwargs.pop('uid_map', "")
        self.gid_map = kwargs.pop('gid_map', "")
        self.map_zero = kwargs.pop('map_zero', False)

        if kwargs.pop('vm', False):
            self.clone_flags |= CLONE_VM
        if kwargs.pop('fs', False):
            self.clone_flags |= CLONE_FS
        if kwargs.pop('files', False):
            self.clone_flags |= CLONE_FILES
        if kwargs.pop('sighand', False):
            self.clone_flags |= CLONE_SIGHAND
        if kwargs.pop('ptrace', False):
            self.clone_flags |= CLONE_PTRACE
        if kwargs.pop('vfork', False):
            self.clone_flags |= CLONE_VFORK
        if kwargs.pop('parent', False):
            self.clone_flags |= CLONE_PARENT
        if kwargs.pop('thread', False):
            self.clone_flags |= CLONE_THREAD
        if kwargs.pop('newns', False):
            self.clone_flags |= CLONE_NEWNS
        if kwargs.pop('sysvsem', False):
            self.clone_flags |= CLONE_SYSVSEM
        if kwargs.pop('settls', False):
            self.clone_flags |= CLONE_SETTLS
        if kwargs.pop('settid', False):
            self.clone_flags |= CLONE_PARENT_SETTID
        if kwargs.pop('child_cleartid', False):
            self.clone_flags |= CLONE_CHILD_CLEARTID
        if kwargs.pop('detached', False):
            self.clone_flags |= CLONE_DETACHED
        if kwargs.pop('untraced', False):
            self.clone_flags |= CLONE_UNTRACED
        if kwargs.pop('child_settid', False):
            self.clone_flags |= CLONE_CHILD_SETTID
        if kwargs.pop('newuts', False):
            self.clone_flags |= CLONE_NEWUTS
        if kwargs.pop('newipc', False):
            self.clone_flags |= CLONE_NEWIPC
        if kwargs.pop('newuser', False):
            self.clone_flags |= CLONE_NEWUSER
        if kwargs.pop('newpid', False):
            self.clone_flags |= CLONE_NEWPID
        if kwargs.pop('newnet', False):
            self.clone_flags |= CLONE_NEWNET
        if kwargs.pop('io', False):
            self.clone_flags |= CLONE_IO

        Process.__init__(self, *args, **kwargs)

