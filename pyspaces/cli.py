#!/usr/bin/env python
# coding=utf-8


import os
import click
from .process import Container



class Space(object):

    def __init__(self):
        pass


pass_space = click.make_pass_decorator(Space)


@click.group()
@click.option('--verbose', '-v', is_flag=True,
              help='Enables verbose mode.')
@click.version_option('1.0.5')
@click.pass_context
def cli(ctx, verbose):
    """Space is tool for managing linux namespaces containers."""
    ctx.obj = Space()
    ctx.obj.verbose = verbose


@cli.command()
@click.argument('argv', nargs=-1, required=True)
@click.option('--ipc', '-i', is_flag=True,
                help='New IPC namespace')
@click.option('--fs', '-m', is_flag=True,
                help='New mount namespace')
@click.option('--net', '-n', is_flag=True,
                help='New network namespace')
@click.option('--pid', '-p', is_flag=True,
                help='New PID namespace')
@click.option('--uts', '-u', is_flag=True,
                help='New UTS namespace')
@click.option('--user', '-U', is_flag=True,
                help='New user namespace')
@click.option('--uid', '-M',
                help='Specify UID map for user namespace')
@click.option('--gid', '-G',
                help='Specify GID map for user namespace')
@click.option('--id', '-z', is_flag=True,
                help='Map user\'s UID and GID to 0 in user namespace'
                '(equivalent to: -M \'0 <uid> 1\' -G \'0 <gid> 1\')')
@pass_space
def execute(space, argv, ipc, fs, net, pid, uts, user, uid, gid, id):
    """Run process in new namespaces.

    $ space execute --pid --fs --user --uid '0 1000 1' bash

    Create a child process that executes a shell command in new
    namespace(s); allow UID and GID mappings to be specified when
    creating a user namespace.

    Analog of userns_child_exec from user namespaces man.

    """
    c = Container(target=os.execvp, args=(argv[0], argv),
              uid_map=uid, gid_map=gid, map_zero=id,
              newpid=pid, newuser=user, newns=fs,
              newuts=uts, newipc=ipc, newnet=net)
    c.start()
    if space.verbose:
        click.echo("PID of child created by clone() is %ld\n" % c.pid)
    c.join()
    if space.verbose:
        click.echo("Child returned: pid %s, status %s" % (c.pid, c.exitcode))
