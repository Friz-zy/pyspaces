#!/usr/bin/env python
# coding=utf-8


import os
import argparse
from . import __version__
from .process import Container, Chroot


def cli():
    """Parse cli args."""
    p = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog='space',
        description='Space is tool for managing linux namespaces containers.',
        epilog='Version %s' % __version__,
    )
    p.add_argument('--verbose', '-v', action='store_true',
        default=False, help='Enables verbose mode.'
    )

    subps = p.add_subparsers()

    # chroot
    pe = subps.add_parser('chroot',
        help='Run program in new root and namespaces.'
    )
    pe.add_argument('path',
        help='New root directory.',
    )
    pe.add_argument('argv',
        help='Command with args for executing.',
    )
    pe.add_argument('--ipc', '-i', default=False,
        action='store_true', help='New IPC namespace'
    )
    pe.add_argument('--net', '-n', default=False,
        action='store_true', help='New network namespace'
    )
    pe.add_argument('--pid', '-p', default=False,
        action='store_true', help='New PID namespace'
    )
    pe.add_argument('--uts', '-u', default=False,
        action='store_true', help='New UTS namespace'
    )
    pe.add_argument('--uid', '-M', default='',
        help='Specify UID map for user namespace'
    )
    pe.add_argument('--gid', '-G', default='',
        help='Specify GID map for user namespace'
    )
    pe.add_argument('--id', '-z', default=False,
        action='store_true',
        help='Map user\'s UID and GID to 0 in user namespace'
             '(equivalent to: -M \'0 <uid> 1\' -G \'0 <gid> 1\')'
    )
    pe.set_defaults(func=chroot)

    # execute
    pe = subps.add_parser('execute',
        help='Run program in new namespaces.'
    )
    pe.add_argument('argv',
        help='Command with args for executing.',
    )
    pe.add_argument('--ipc', '-i', default=False,
        action='store_true', help='New IPC namespace'
    )
    pe.add_argument('--fs', '-m', default=False,
        action='store_true', help='New mount namespace'
    )
    pe.add_argument('--net', '-n', default=False,
        action='store_true', help='New network namespace'
    )
    pe.add_argument('--pid', '-p', default=False,
        action='store_true', help='New PID namespace'
    )
    pe.add_argument('--uts', '-u', default=False,
        action='store_true', help='New UTS namespace'
    )
    pe.add_argument('--user', '-U', default=False,
        action='store_true', help='New user namespace'
    )
    pe.add_argument('--uid', '-M', default='',
        help='Specify UID map for user namespace'
    )
    pe.add_argument('--gid', '-G', default='',
        help='Specify GID map for user namespace'
    )
    pe.add_argument('--id', '-z', default=False,
        action='store_true',
        help='Map user\'s UID and GID to 0 in user namespace'
             '(equivalent to: -M \'0 <uid> 1\' -G \'0 <gid> 1\')'
    )
    pe.set_defaults(func=execute)

    args, extra = p.parse_known_args()
    args.func(args, extra)

def execute(args, argv):
    """Run program in new namespaces.

    $ space execute --pid --fs --user --uid '0 1000 1' bash

    Create a child process that executes a shell command in new
    namespace(s); allow UID and GID mappings to be specified when
    creating a user namespace.

    Analog of userns_child_exec from user namespaces man.

    """
    argv.insert(0, args.argv)
    c = Container(target=os.execvp, args=(argv[0], argv),
              uid_map=args.uid, gid_map=args.gid, map_zero=args.id,
              newpid=args.pid, newuser=args.user, newns=args.fs,
              newuts=args.uts, newipc=args.ipc, newnet=args.net)
    c.start()
    if args.verbose:
        print("PID of child created by clone() is %ld\n" % c.pid)
    c.join()
    if args.verbose:
        print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))

def chroot(args, argv):
    """Run program in new root and namespaces.

    $ space chroot --pid --uid '0 1000 1'  ~/.local/share/lxc/ubuntu/rootfs/ /bin/ls /home/

    Create a child process that executes a shell command in new
    root directory, ns, user and additional namespaces; allow UID
    and GID mappings to be specified when creating a user namespace.

    Analog of chroot program.

    """
    argv.insert(0, args.argv)
    c = Chroot(path=args.path, target=os.execvp,
              args=(argv[0], argv), newpid=args.pid,
              uid_map=args.uid, gid_map=args.gid, map_zero=args.id,
              newuts=args.uts, newipc=args.ipc, newnet=args.net)
    c.start()
    if args.verbose:
        print("PID of child created by clone() is %ld\n" % c.pid)
    c.join()
    if args.verbose:
        print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))


if __name__ == '__main__':
    cli()
