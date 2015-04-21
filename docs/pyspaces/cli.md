Module pyspaces.cli
-------------------

Functions
---------
- **chroot** (args, argv)

    Run program in new root and namespaces.

    $ space chroot --pid --uid '0 1000 1'  ~/.local/share/lxc/ubuntu/rootfs/ /bin/ls /home/
  
    Create a child process that executes a shell command in new
root directory, ns, user and additional namespaces; allow UID
and GID mappings to be specified when creating a user namespace.
  
    Analog of chroot program.

- **cli** ()

    Parse cli args.

- **execute** (args, argv)

    Run program in new namespaces.

    $ space execute --pid --fs --user --uid '0 1000 1' bash
  
    Create a child process that executes a shell command in new
namespace(s); allow UID and GID mappings to be specified when
creating a user namespace.
  
    Analog of userns_child_exec from user namespaces man.
