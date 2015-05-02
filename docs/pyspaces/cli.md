Module pyspaces.cli
-------------------

* This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)
  

* License: MIT or BSD or Apache 2.0  
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

Functions
---------
- **chroot** (args, argv)

    Run program in new root and namespaces.

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

- **cli** ()

    Parse cli args.

- **execute** (args, argv)

    Run program in new namespaces.

    $ space execute --pid --fs --user --uid '0 1000 1' bash
  
    Create a child process that executes a shell command in new
namespace(s); allow UID and GID mappings to be specified when
creating a user namespace.
  
    Analog of userns_child_exec from user namespaces man.
