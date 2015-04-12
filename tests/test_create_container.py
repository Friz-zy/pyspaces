#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
#import pytest
from process import Container


def execute(argv):
    """Execute programm with arguments.

    Args:
      *args (list): arguments

    """
    os.execvp(argv[0], argv)

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
