#!/usr/bin/env python
# coding=utf-8


import os
import argparse
from . import __version__
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
    p_ipc.add_argument('--ipc', '-i', default=False,
        action='store_true', help='New IPC namespace'
    )
    p_mount = argparse.ArgumentParser(add_help=False)
    p_mount.add_argument('--fs', '--mnt', '-m', default=False,
        action='store_true', help='New mount namespace'
    )
    p_net = argparse.ArgumentParser(add_help=False)
    p_net.add_argument('--net', '-n', default=False,
        action='store_true', help='New network namespace'
    )
    p_pid = argparse.ArgumentParser(add_help=False)
    p_pid.add_argument('--pid', '-p', default=False,
        action='store_true', help='New PID namespace'
    )
    p_uts = argparse.ArgumentParser(add_help=False)
    p_uts.add_argument('--uts', '-u', default=False,
        action='store_true', help='New UTS namespace'
    )
    p_user = argparse.ArgumentParser(add_help=False)
    p_user.add_argument('--user', '-U', default=False,
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
            p_pid, p_uts, p_user,
        ],
        help='Run program in new namespaces.'
    )
    pe.set_defaults(func=execute)

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
    if args.all:
        args.pid = True
        args.user = True
        args.fs = True
        args.uts = True
        args.ipc = True
        args.net = True

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
    if args.all:
        args.pid = True
        args.user = True
        args.fs = True
        args.uts = True
        args.ipc = True
        args.net = True

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
