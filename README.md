# pyspaces
Works with Linux namespaces througth glibc with pure python

[![License](https://pypip.in/license/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Latest Version](https://pypip.in/version/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Downloads](https://pypip.in/download/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Docs](https://readthedocs.org/projects/pyspaces/badge/)](https://pyspaces.readthedocs.org/en/latest/)


## Goals

There is so many beautiful tools like [docker](https://github.com/docker/docker), [rocket](https://github.com/coreos/rkt) and [vagga](https://github.com/tailhook/vagga) written on go and rust, but no one on python.
I think that is because there is no easy way to works with linux namespaces on python:

* you can use [asylum](https://pypi.python.org/pypi/asylum/0.4.1) - project that looks like dead and with codebase hosted not on mainstream hub like github
* or you can use [python-libvirt](https://pypi.python.org/pypi/libvirt-python/1.2.13) bindings with big layer of abstraction
* or just use native glibc library with ctypes
* otherwise subprocess.Popen your choice

I want to change it: i want to create native python bindings to glibc with interface of python multiprocessing.Process.

## Example

First simple example:
```python
import os
from pyspaces import Container


def execute(argv):
    os.execvp(argv[0], argv)

cmd = "mount -t proc proc /proc; ps ax"
c = Container(target=execute, args=(('bash', '-c', cmd),),
              uid_map='0 1000 1',
              newpid=True, newuser=True, newns=True
              )
c.start()
print("PID of child created by clone() is %ld\n" % c.pid)
c.join()
print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))
```
output:
```bash
PID of child created by clone() is 15978

PID TTY      STAT   TIME COMMAND
1   pts/19   S+     0:00 bash -c mount -t proc proc /proc; ps ax
3   pts/19   R+     0:00 ps ax

Child returned: pid 15978, status 0
```

## CLI

```bash
space -v execute --pid --fs --user --uid '0 1000 1' bash -c 'mount -t proc /proc; ps ax'
```

```bash
space chroot --pid --uid '0 1000 1' ~/.local/share/lxc/ubuntu/rootfs/ /bin/ls /home/
```
Note:
>>> If the program you're trying to exec is dynamic linked, and the dynamic linker is not present in /lib in the chroot environment - you would get the "OSError: [Errno 2] No such file or directory" error. You'd need all the other files the dynamic-linked program depends on, including shared libraries and any essential configuration/table/etc in the new root directories.  
[src](http://www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)
