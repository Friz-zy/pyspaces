#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import os
import sys
import errno
from .libc import *
from signal import SIGKILL, SIGCHLD

try:
    from multiprocessing.forking import Popen
except ImportError:
    from multiprocessing.popen_fork import Popen


STACK_SIZE = 1024 * 1024
"""STACK_SIZE (1024 * 1024)"""

# cloning flags
# src: linux/include/uapi/linux/sched.h
CLONE_VM = 0x00000100  
"""set if VM shared between processes"""
CLONE_FS = 0x00000200  
"""set if fs info shared between processes"""
CLONE_FILES = 0x00000400  
"""set if open files shared between processes"""
CLONE_SIGHAND = 0x00000800  
"""set if signal handlers and blocked signals shared"""
CLONE_PTRACE = 0x00002000  
"""set if we want to let tracing continue on the child too"""
CLONE_VFORK = 0x00004000  
"""set if the parent wants the child to wake it up on mm_release"""
CLONE_PARENT = 0x00008000  
"""set if we want to have the same parent as the cloner"""
CLONE_THREAD = 0x00010000  
"""Same thread group?"""
CLONE_NEWNS = 0x00020000  
"""New mount namespace group"""
CLONE_SYSVSEM = 0x00040000  
"""share system V SEM_UNDO semantics"""
CLONE_SETTLS = 0x00080000  
"""create a new TLS for the child"""
CLONE_PARENT_SETTID = 0x00100000  
"""set the TID in the parent"""
CLONE_CHILD_CLEARTID = 0x00200000  
"""clear the TID in the child"""
CLONE_DETACHED = 0x00400000  
"""Unused, ignored"""
CLONE_UNTRACED = 0x00800000  
"""set if the tracing process can't force CLONE_PTRACE on this clone"""
CLONE_CHILD_SETTID = 0x01000000  
"""set the TID in the child"""
CLONE_NEWUTS = 0x04000000  
"""New utsname namespace"""
CLONE_NEWIPC = 0x08000000  
"""New ipc namespace"""
CLONE_NEWUSER = 0x10000000  
"""New user namespace"""
CLONE_NEWPID = 0x20000000  
"""New pid namespace"""
CLONE_NEWNET = 0x40000000  
"""New network namespace"""
CLONE_IO = 0x80000000  
"""Clone io context"""


class Clone(Popen):
    """Inheritance from `multiprocessing.forking.Popen`.

    We define a Popen class similar to the one from subprocess, but
    whose constructor takes a process object as its argument.

    Raises:
      OSError: can not execute glibc.clone function
      RuntimeError: parent doesn't close its pipe descriptor
      IOError: do not have permission to write to a file.
        Child will be killed with signal.SIGKILL.

    """
    def __init__(self, process_obj):
        """Execute linux clone.

        Create a child process in new namespace(s);
        allow UID and GID mappings to be specified when
        creating a user namespace.

        Raises:
          OSError: can not execute glibc.clone function

        """
        sys.stdout.flush()
        sys.stderr.flush()
        self.process_obj = process_obj
        self.returncode = None
        self.pipe_fd = os.pipe()

        # clone attributes
        flags = process_obj.__dict__.get('clone_flags', 0)
        uid_map = process_obj.__dict__.get('uid_map', "")
        gid_map = process_obj.__dict__.get('gid_map', "")
        map_zero = process_obj.__dict__.get('map_zero', False)
        proc = process_obj.__dict__.get('proc', '/proc')

        # Create the child in new namespace(s)
        child = CFUNCTYPE(c_int)(self.child)
        child_stack = create_string_buffer(STACK_SIZE)
        child_stack_pointer = c_void_p(cast(child_stack, c_void_p).value + STACK_SIZE)

        self.pid = libc.clone(child, child_stack_pointer, flags | SIGCHLD)

        if self.pid == -1:
            e = get_errno()
            raise OSError(e, os.strerror(e))

        # Update the UID and GID maps in the child
        def arg2map(arg):
            #    int: map given uid to root
            #    str: like int or in format
            #    ' '.join((<start uid in new ns>,
            #              <start uid in current ns>,
            #              <range to mapping>
            #    )). Example "0 1000 1" will map 1000 uid as root,
            #    "0 1000 1,1 1001 1" will map also 1001 as uid 1.
            #    list: list of int or str
            if type(arg) is int:
                return "0 %d 1" % arg
            if not hasattr(arg, '__iter__'):
                arg = arg.split(',')
            if ' ' not in arg[0]:
                arg = ['%d %s 1' % (i, d) for i, d in enumerate(arg)]
            return '\n'.join(arg)

        if uid_map or map_zero:
            map_path = "%s/%s/uid_map" % (proc, self.pid)
            if map_zero or type(uid_map) is bool:
                uid_map = "0 %d 1" % os.getuid()
            else:
                uid_map = arg2map(uid_map)
            self.update_map(uid_map, map_path)

        if gid_map or map_zero:
            # Writing "deny" to the /proc/[pid]/setgroups file before writing to
            # /proc/[pid]/gid_map will permanently disable setgroups(2) in a user
            # namespace and allow writing to /proc/[pid]/gid_map without having the
            # CAP_SETGID capability in the parent user namespace.
            with open("%s/%s/setgroups" % (proc, self.pid), 'w') as f:
                f.write("deny")
            map_path = "%s/%s/gid_map" % (proc, self.pid)
            if map_zero or type(gid_map) is bool:
                gid_map = "0 %d 1" % os.getgid()
            else:
                gid_map = arg2map(gid_map)
            self.update_map(gid_map, map_path)

        # Close the write end of the pipe, to signal to the child that we
        # have updated the UID and GID maps
        os.close(self.pipe_fd[1])
        self.sentinel = self.pipe_fd[0]

    def child(self):
        """Start function for cloned child.

        Wait until the parent has updated the UID and GID mappings.
        See the comment in main(). We wait for end of file on a
        pipe that will be closed by the parent process once it has
        updated the mappings.

        Raises:
          RuntimeError: parent doesn't close its pipe descriptor

        """
        # Close our descriptor for the write
        # end of the pipe so that we see EOF
        # when parent closes its descriptor
        os.close(self.pipe_fd[1])
        if os.read(self.pipe_fd[0], 1):
            raise RuntimeError(
                'Failure in child:'
                ' parent doesn\'t close its descriptor'
            )

        if 'random' in sys.modules:
            import random
            random.seed()
        code = self.process_obj._bootstrap()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(code)

    def update_map(self, mapping, map_file):
        """

        Update the mapping file 'map_file', with the value provided in
        'mapping', a string that defines a UID or GID mapping. A UID or
        GID mapping consists of one or more newline-delimited records
        of the form:

            ID_inside-ns    ID-outside-ns   length

        Requiring the user to supply a string that contains newlines is
        of course inconvenient for command-line use. Thus, we permit the
        use of commas to delimit records in this string, and replace them
        with newlines before writing the string to the file.

        Raises:
          IOError: do not have permission to write to a file.
            Child will be killed with signal.SIGKILL.

        """
        #Replace commas in mapping string with newlines
        mapping = mapping.replace(',', '\n')

        try:
            with open(map_file, 'w') as f:
                f.write(mapping)
        except IOError as e:
            os.kill(self.pid, SIGKILL)
            raise IOError(
                "Can not write %s: %s\nAborting!" % (map_file, e)
            )
