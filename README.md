# pyspaces
Works with Linux namespaces througth glibc with pure python

## Goals

There is so many beautiful tools like [docker](), [rocket]() and [vagga]() written on go and rust, but no one on python.
I think that is because there is no easy way to works wit linux namespaces on python:

* you can use [asylum] - project that looks like dead and with codebase hosted not on mainstream hub like github
* or you can use python-libvirt bindings with big layer of abstraction
* or just use native glibc library with ctypes
* otherwise subprocess.Popen your choice

I want to change it: i want to create native python bindings to glibc with interface of python multiprocessing.Process.

## Example

First simpe example
```python
from pyspaces import Container


def execute(argv):
    os.execvp(argv[0], argv)

cmd = "mount -t proc proc /proc; ps ax"
c = Container(target=execute, args=(('bash', '-c', cmd),
              uid_map='0 1000 1',
              newpid=True, newuser=True, newns=True
              )
c.start()
print("PID of child created by clone() is %ld\n" % c.pid)
c.join()
print("Child returned: pid %s, status %s" % (c.pid, c.exitcode))
```
```bash
PID of child created by clone() is 15978

PID TTY      STAT   TIME COMMAND
1   pts/19   S+     0:00 bash -c mount -t proc proc /proc; ps ax
3   pts/19   R+     0:00 ps ax

Child returned: pid 15978, status 0
```