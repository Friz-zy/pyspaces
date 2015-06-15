#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import pytest
from pyspaces import Container, Chroot, Inject, setns


def execute(argv):
    """Execute programm with arguments.

    Args:
      *args (list): arguments

    """
    os.execvp(argv[0], argv)

def test_basic_container(capfd):
    """Check basic namespace

    ```
    bash# mount -t proc proc /proc
    bash# ps ax
    PID TTY      STAT   TIME COMMAND
    1  pts/3    S      0:00 bash
    22 pts/3    R+     0:00 ps ax
    ```

    """
    cmd = "mount -t proc proc /proc; ps ax"
    c = Container(target=execute, args=(('bash', '-c', cmd),),
                  uid_map='0 1000 1',
                  newpid=True, newuser=True, newns=True
                  )
    c.start()
    c.join()
    out, err = capfd.readouterr()
    print out, err
    assert len(out.splitlines()) == 3

def test_basic_chroot(capfd):
    """Check basic chroot"""
    c = Chroot(target=execute, args=(('/bin/ls', '/home/'),),
                  uid_map=True, newpid=True,
                  path=os.path.expanduser('~/.local/share/lxc/ubuntu/rootfs/'))
    c.start()
    c.join()
    out, err = capfd.readouterr()
    print out, err
    assert out == 'ubuntu\n'

def test_basic_inject(capfd):
    """Check basic inject"""
    c = Container(target=execute, args=(('bash','-c',
                'mount -t proc /proc; sleep 0.1'),),
                uid_map='1000', all=True
    )
    c.start()
    i = Inject(target=execute, args=(('bash', '-c', 'id'),),
                target_pid=c.pid, all=True
    )
    i.start()
    i.join()
    out, err = capfd.readouterr()
    print out, err
    assert out.split()[:2] == ["uid=0(root)", "gid=65534(nogroup)"]

def test_basic_setns(capfd):
    """Check basic inject"""
    import subprocess as s
    c = Container(target=execute, args=(('bash','-c',
                'mount -t proc /proc; sleep 2'),),
                uid_map='1000', all=True
    )
    c.start()
    with setns(c.pid, all=True):
        outt = s.check_output("id", shell=True)
    out, err = capfd.readouterr()
    print out, err
    print outt
    assert outt.split()[:2] == ["uid=0(root)", "gid=65534(nogroup)"]

if __name__ == "__main__":
    """

    ```
    bash# mount -t proc proc /proc
    bash# ps ax
    PID TTY      STAT   TIME COMMAND
    1  pts/3    S      0:00 bash
    22 pts/3    R+     0:00 ps ax
    ```

    """
    c = Container(target=execute, args=(('bash',),),
                  uid_map='0 1000 1',
                  newpid=True, newuser=True, newns=True
                  )
    c.start()
    print("PID of child created by clone() is %ld\n" % c.pid)
    c.join()
    print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))
