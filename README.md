# pyspaces
Works with Linux namespaces througth glibc with pure python

[![License](https://pypip.in/license/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Latest Version](https://pypip.in/version/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Downloads](https://pypip.in/download/pyspaces/badge.svg)](https://pypi.python.org/pypi/pyspaces/)
[![Docs](https://readthedocs.org/projects/pyspaces/badge/)](https://pyspaces.readthedocs.org/en/latest/)

discuss: [reddit](https://www.reddit.com/r/Python/comments/33z84l/linux_namespaces_througth_glibc_with_pure_python/), [habrahabr](http://habrahabr.ru/company/wargaming/blog/256647/)

## Goals

There is so many beautiful tools like [docker](https://github.com/docker/docker), [rocket](https://github.com/coreos/rkt) and [vagga](https://github.com/tailhook/vagga) written on go and rust, but no one on python.
I think that is because there is no easy way to works with linux namespaces on python:

* you can use [asylum](https://pypi.python.org/pypi/asylum/0.4.1) - project that looks like dead and with codebase hosted not on mainstream hub like github
* or you can use [python-libvirt](https://pypi.python.org/pypi/libvirt-python/1.2.13) bindings with big layer of abstraction
* or just use native glibc library with ctypes
* otherwise subprocess.Popen your choice

I want to change it: i want to create native python bindings to glibc with interface of python multiprocessing.Process.

PS: you can look at [python-nsenter](https://github.com/zalando/python-nsenter) too, it's looks awesome.

PPS: new project from author of asylum - [butter](https://pypi.python.org/pypi/butter/0.10)

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
space execute -v --pid --mnt --user --uid 1000 --gid 1000 bash -c 'mount -t proc /proc; ps ax'
```

```bash
space chroot --pid --uid '0 1000 1' ~/.local/share/lxc/ubuntu/rootfs/ /bin/ls /home/
```

```bash
space inject --net --mnt 19840 bash
```

Note: If the program you're trying to exec is dynamic linked, and the dynamic linker is not present in /lib in the chroot environment - you would get the "OSError: [Errno 2] No such file or directory" error. You'd need all the other files the dynamic-linked program depends on, including shared libraries and any essential configuration/table/etc in the new root directories. [src](http://www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)

## Security

- https://opensource.com/business/14/7/docker-security-selinux
- https://opensource.com/business/14/9/security-for-docker
- http://www.slideshare.net/jpetazzo/docker-linux-containers-lxc-and-security
- http://www.itworld.com/article/2920349/security/for-containers-security-is-problem-1.html
- https://mjg59.dreamwidth.org/33170.html
- http://blog.sei.cmu.edu/post.cfm/container-security-devops-176

Read essential in [security.md](https://github.com/Friz-zy/pyspaces/blob/master/security.md) file

## Changelog
[on github](https://github.com/Friz-zy/pyspaces/blob/master/CHANGELOG.md)  
[digest](https://allmychanges.com/p/python/pyspaces/)  

## TODO

- [x] namespaces: clone & Container
- [x] CLI
- [x] Chroot
- [x] setns & inject
- [ ] cgroups
- [ ] SCM: apparmor & selinux
- [ ] capabilities
- [ ] mount
- [ ] network
- [ ] move CLI to separate package
- [ ] addons
- [ ] container list
- [ ] support for lxc, vagga, rocket, docker, etc...
- [ ] ...
- [ ] one tool for rule them all!!1