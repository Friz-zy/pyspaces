#!/usr/bin/env python
# coding=utf-8
"""This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

"""


import os
import argparse
from . import __version__
from .setns import setns
from .process import Container, Chroot


def cli():
    """Parse cli args."""
    # parent parser for all
    p_main = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        prog='space',
        description='Space is tool for managing linux namespaces containers.',
        epilog='Version %s' % __version__,
    )
    p_main.add_argument('--verbose', '-v', action='store_true',
        default=False, help='Enables verbose mode.'
    )

    # main parser for cli
    p_case = argparse.ArgumentParser(add_help=False, parents=[p_main])

    # additional parsers
    p_all = argparse.ArgumentParser(add_help=False)
    p_all.add_argument('--all', '-a', default=False,
        action='store_true', help='Use all 6 namespaces'
    )
    p_ipc = argparse.ArgumentParser(add_help=False)
    p_ipc.add_argument('--ipc', '-i', default=None,
        action='store_true', help='New IPC namespace'
    )
    p_mount = argparse.ArgumentParser(add_help=False)
    p_mount.add_argument('--mnt', '--fs', '-m', default=None,
        action='store_true', help='New mount namespace'
    )
    p_net = argparse.ArgumentParser(add_help=False)
    p_net.add_argument('--net', '-n', default=None,
        action='store_true', help='New network namespace'
    )
    p_pid = argparse.ArgumentParser(add_help=False)
    p_pid.add_argument('--pid', '-p', default=None,
        action='store_true', help='New PID namespace'
    )
    p_uts = argparse.ArgumentParser(add_help=False)
    p_uts.add_argument('--uts', '-u', default=None,
        action='store_true', help='New UTS namespace'
    )
    p_user = argparse.ArgumentParser(add_help=False)
    p_user.add_argument('--user', '-U', default=None,
        action='store_true', help='New user namespace'
    )
    p_uid = argparse.ArgumentParser(add_help=False)
    p_uid.add_argument('--uid', '-M', default='',
        help='Specify UID map for user namespace'
    )
    p_gid = argparse.ArgumentParser(add_help=False)
    p_gid.add_argument('--gid', '-G', default='',
        help='Specify GID map for user namespace'
    )
    p_id = argparse.ArgumentParser(add_help=False)
    p_id.add_argument('--id', '-z', default=False,
        action='store_true',
        help='Map user\'s UID and GID to 0 in user namespace'
             '(equivalent to: -M \'0 <uid> 1\' -G \'0 <gid> 1\')'
    )
    p_argv = argparse.ArgumentParser(add_help=False)
    p_argv.add_argument('argv',
        help='Command with args for executing.',
    )

    subps = p_case.add_subparsers(metavar="<command>")
    # chroot
    pe = subps.add_parser('chroot', add_help=False,
        parents=[p_main,
            p_all, p_uid, p_gid, p_id,
            p_ipc, p_net, p_pid, p_uts,
        ],
        help='Run program in new root and namespaces.'
    )
    pe.add_argument('path',
        help='New root directory.',
    )
    # add argv not as parent parser because of
    # sequence of positional args
    pe.add_argument('argv',
        help='Command with args for executing.',
    )
    pe.set_defaults(func=chroot)
    # execute
    pe = subps.add_parser('execute', add_help=False,
        parents=[p_main, p_argv,
            p_all, p_uid, p_gid, p_id,
            p_ipc, p_mount, p_net,
            p_pid, p_user, p_uts,
        ],
        help='Run program in new namespaces.'
    )
    pe.set_defaults(func=execute)
    # inject
    pe = subps.add_parser('inject', add_help=False,
        parents=[p_main, p_all,
            p_ipc, p_mount, p_net,
            p_pid, p_user, p_uts,
            p_uid, p_gid, p_id,
        ],
        help='Run program in namespaces of another process.'
    )
    pe.add_argument('target_pid',
        help='Pid of target process.',
    )
    # add argv not as parent parser because of
    # sequence of positional args
    pe.add_argument('argv',
        help='Command with args for executing.',
    )
    pe.add_argument('--proc', default='/proc',
        help='root directory of proc fs.',
    )
    pe.set_defaults(func=inject)

    args, extra = p_case.parse_known_args()
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
              newpid=args.pid, newuser=args.user, newns=args.mnt,
              newuts=args.uts, newipc=args.ipc, newnet=args.net,
              all=args.all
    )
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

    Note: If the program you're trying to exec is dynamic
    linked, and the dynamic linker is not present in /lib
    in the chroot environment - you would get the
    "OSError: [Errno 2] No such file or directory" error.
    You'd need all the other files the dynamic-linked
    program depends on, including shared libraries and
    any essential configuration/table/etc in the new
    root directories.
    [src](http://www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)

    """
    argv.insert(0, args.argv)
    c = Chroot(path=args.path, target=os.execvp,
              args=(argv[0], argv), all=args.all, newpid=args.pid,
              uid_map=args.uid, gid_map=args.gid, map_zero=args.id,
              newuts=args.uts, newipc=args.ipc, newnet=args.net
    )
    c.start()
    if args.verbose:
        print("PID of child created by clone() is %ld\n" % c.pid)
    c.join()
    if args.verbose:
        print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))

def inject(args, argv):
    """Run program in namespaces of another process.

    $ space inject --all 12603 bash

    """
    argv.insert(0, args.argv)
    if args.verbose:
        print("PID is %ld\n" % os.getpid())
    with setns(args.target_pid, False, args.proc,
               newpid=args.pid, newuser=args.user, newns=args.mnt,
               newuts=args.uts, newipc=args.ipc, newnet=args.net,
               all=args.all):
        os.execvp(argv[0], argv)


if __name__ == '__main__':
    cli()
