Module pyspaces.process
-----------------------

This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)

License: MIT or BSD or Apache 2.0  
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

Variables
---------
- **ca**

Classes
-------
#### Chroot 
Class wrapper over `pyspaces.Container`
  
Chroot objects represent activity that is run in a separate process
in new filesystem and user namespaces.
  
The class is analagous to `threading.Thread`.

##### Ancestors (in MRO)
- pyspaces.process.Chroot

- pyspaces.process.Container

- multiprocessing.process.Process

- __builtin__.object

##### Instance variables
- **args**

- **authkey**

- **clone_flags**

- **daemon**

    Return whether process is a daemon

- **exitcode**

    Return exit code of process or `None` if it has yet to stop

- **gid_map**

- **ident**

    Return identifier (PID) of process or `None` if it has yet to start

- **kwargs**

- **map_zero**

- **name**

- **pid**

    Return identifier (PID) of process or `None` if it has yet to start

- **proc**

- **uid_map**

##### Methods
- **__init__** (self, path, target, args=(), kwargs={}, *cargs, **ckwargs)

    Set target and clone flags and execute Container.__init__
  
    Set newuser and newns clone flags, set self.chroot
as target with necessary args and kwargs. Then
execute Container.__init__ with updated parameters.
  
    Note:    
If the program you're trying to exec is dynamic
linked, and the dynamic linker is not present in /lib
in the chroot environment - you would get the
"OSError: [Errno 2] No such file or directory" error.  
You'd need all the other files the dynamic-linked
program depends on, including shared libraries and
any essential configuration/table/etc in the new
root directories.
[src](http://www.ciiycode.com/0JiJzPgggqPg/why-doesnt-exec-work-after-chroot)
  
    Args:  

    * path (str): path to chroot new root

    * target (python function): python function
for executing after chroot

    * args (list): args for target,
default is ()

    * kwargs (dict): kwargs for target,
default is {}

    * *cargs (list): arguments for Container.__init__

    * **ckwargs (dict): arguments for Container.__init__

- **chdir** (self)

    Change working dir with os.chdir.
  
    Change current directory to new
  
    Required:  
self.kwargs['workdir']

- **chroot** (self)

    Change root with os.chroot.
  
    Change working directory to rootdir,
then execute chroot and then again
change working dir to workdir.
  
    Required:  
self.kwargs['rootdir']

- **chtty** (self)

    Change stdin, stdout, stderr.
  
    Required:  
self.kwargs['stdin']
self.kwargs['stdout']
self.kwargs['stderr']

- **daemonize** (self)

    Execute target as daemon
  
    Required:  
self.kwargs['daemonize'].

- **exceptexec** (self)

    Dummy function.

- **exceptup** (self)

    Dummy function.

- **is_alive** (self)

    Return whether process is alive

- **join** (self, timeout=None)

    Wait until child process terminates

- **postexec** (self)

    Dummy function.

- **postup** (self)

    Dummy function.

- **preexec** (self)

    Dummy function.

- **preup** (self)

    Dummy function.

- **run** (self)

    Method to be run in sub-process; can be overridden in sub-class

- **runup** (self)

    Main wrapper over target function.
  
    Execution order:  

    0.1) new ns and sigmask (Clone)

    0.2) set uid, gid (Clone)

    1) self.preup (mount, etc)

    4) self.daemonize

    5) self.chroot

    6) self.chdir

    7) self.chtty ?vagga before ns

    8) self.postup - in finally block

    9) self.exceptup - in except block

    10) self.preexec (networking, etc)

    11) execute self.target

    12) self.postexec - in finally block

    13) self.exceptexec - in except block
  
    Required:  
self.kwargs['target']
self.kwargs['args']
self.kwargs['kwargs']
  
    Return:  

    * int: return of target function
or 0 if no one exception was
raised
  
    Raise:  
any exception
  
    TODO:  
apparmor  
selinux  

- **start** (self)

    Start child process

- **terminate** (self)

    Terminate process; sends SIGTERM signal or uses TerminateProcess()

#### Container 
Class wrapper over `multiprocessing.Process`.
  
Container objects represent activity that is run in a separate process.
  
The class is analagous to `threading.Thread`.

##### Ancestors (in MRO)
- pyspaces.process.Container

- multiprocessing.process.Process

- __builtin__.object

##### Descendents
- pyspaces.process.Chroot

- pyspaces.process.Inject

##### Instance variables
- **args**

- **authkey**

- **clone_flags**

- **daemon**

    Return whether process is a daemon

- **exitcode**

    Return exit code of process or `None` if it has yet to stop

- **gid_map**

- **ident**

    Return identifier (PID) of process or `None` if it has yet to start

- **kwargs**

- **map_zero**

- **name**

- **pid**

    Return identifier (PID) of process or `None` if it has yet to start

- **proc**

- **uid_map**

##### Methods
- **__init__** (self, *args, **kwargs)

    Set clone flags and execute Process.__init__
  
    Args:  

    * *args (list): arguments for Process.__init__

    * **kwargs (dict): arguments for Process.__init__

    * target (callable object): callable object to be
invoked by the run() method

    * args (tuple): argument tuple for the target
invocation, default is ()

    * kwargs (dict): dict of keyword arguments for
the target invocation, default is {}

    * all (bool): set all 6 namespaces,
default is False

    * newuts, uts (bool): set CLONE_NEWUTS flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * newipc, ipc (bool): set CLONE_NEWIPC flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * newuser, user (bool): set CLONE_NEWUSER flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * newpid, pid (bool): set CLONE_NEWPID flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * newnet, net (bool): set CLONE_NEWNET flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * newns, mnt (bool): set CLONE_NEWNS flag if True,
does not set flag enev with 'all' arg if False,
default is None

    * uid_map (bool, int, str, list): UID mapping
for new namespace:  

    * bool: map current uid as root

    * int: map given uid as root

    * str: like int or in format
' '.join((<start uid in new ns>,
<start uid in current ns>,
<range to mapping>
)). Example "0 1000 1" will map 1000 uid as root,
"0 1000 1,1 1001 1" or "1000,1001"
will map 1000 as root and 1001 as uid 1.

    * list: list of int or str
default is ""

    * gid_map (bool, int, str, list): GID mapping
for new namespace, format the same as uid_map,
default is ""

    * map_zero (bool): Map user's UID and GID to 0
in user namespace, default is False

    * rootdir (str): path to new root, default is None

    * workdir (str): path to new working dir,
default is os.getcwd();
if you set new rootdir, workdir
path should be in new root tree
and default will be '/'

    * stdin (str, int, fd, fo): set new sys.stdin
and 0 file descriptor,
default '/dev/null' if daemonize

    * stdout (str, int, fd, fo): set new sys.stdout
and 1 file descriptor,
default '/dev/null' if daemonize

    * stderr (str, int, fd, fo): set new sys.stderr
and 2 file descriptor,
default '/dev/null' if daemonize

    * daemonize (bool): execute target as
daemon, default is False

    * proc (str): root directory of proc fs,
default is '/proc'

    * vm (bool): set CLONE_VM flag,
default is False

    * fs (bool): set CLONE_FS flag,
default is False

    * files (bool): set CLONE_FILES flag,
default is False

    * sighand (bool): set CLONE_SIGHAND flag,
default is False

    * ptrace (bool): set CLONE_PTRACE flag,
default is False

    * vfork (bool): set CLONE_VFORK flag,
default is False

    * parent (bool): set CLONE_PARENT flag,
default is False

    * thread (bool): set CLONE_THREAD flag,
default is False

    * sysvsem (bool): set CLONE_SYSVSEM flag,
default is False

    * settls (bool): set CLONE_SETTLS flag,
default is False

    * settid (bool): set CLONE_PARENT_SETTID flag,
default is False

    * child_cleartid (bool): set CLONE_CHILD_CLEARTID flag,
default is False

    * detached (bool): set CLONE_DETACHED flag,
default is False

    * untraced (bool): set CLONE_UNTRACED flag,
default is False

    * child_settid (bool): set CLONE_CHILD_SETTID flag,
default is False

    * io (bool): set CLONE_IO flag,
default is False

    * flags (int): flags for clone, default is 0

- **chdir** (self)

    Change working dir with os.chdir.
  
    Change current directory to new
  
    Required:  
self.kwargs['workdir']

- **chroot** (self)

    Change root with os.chroot.
  
    Change working directory to rootdir,
then execute chroot and then again
change working dir to workdir.
  
    Required:  
self.kwargs['rootdir']

- **chtty** (self)

    Change stdin, stdout, stderr.
  
    Required:  
self.kwargs['stdin']
self.kwargs['stdout']
self.kwargs['stderr']

- **daemonize** (self)

    Execute target as daemon
  
    Required:  
self.kwargs['daemonize'].

- **exceptexec** (self)

    Dummy function.

- **exceptup** (self)

    Dummy function.

- **is_alive** (self)

    Return whether process is alive

- **join** (self, timeout=None)

    Wait until child process terminates

- **postexec** (self)

    Dummy function.

- **postup** (self)

    Dummy function.

- **preexec** (self)

    Dummy function.

- **preup** (self)

    Dummy function.

- **run** (self)

    Method to be run in sub-process; can be overridden in sub-class

- **runup** (self)

    Main wrapper over target function.
  
    Execution order:  

    0.1) new ns and sigmask (Clone)

    0.2) set uid, gid (Clone)

    1) self.preup (mount, etc)

    4) self.daemonize

    5) self.chroot

    6) self.chdir

    7) self.chtty ?vagga before ns

    8) self.postup - in finally block

    9) self.exceptup - in except block

    10) self.preexec (networking, etc)

    11) execute self.target

    12) self.postexec - in finally block

    13) self.exceptexec - in except block
  
    Required:  
self.kwargs['target']
self.kwargs['args']
self.kwargs['kwargs']
  
    Return:  

    * int: return of target function
or 0 if no one exception was
raised
  
    Raise:  
any exception
  
    TODO:  
apparmor
selinux

- **start** (self)

    Start child process

- **terminate** (self)

    Terminate process; sends SIGTERM signal or uses TerminateProcess()

#### Inject 
Class wrapper over `multiprocessing.Process`.
  
Create process in namespaces of another one.
  
The class is analagous to `threading.Thread`.

##### Ancestors (in MRO)
- pyspaces.process.Inject

- pyspaces.process.Container

- multiprocessing.process.Process

- __builtin__.object

##### Instance variables
- **args**

- **authkey**

- **clone_flags**

- **daemon**

    Return whether process is a daemon

- **exitcode**

    Return exit code of process or `None` if it has yet to stop

- **gid_map**

- **ident**

    Return identifier (PID) of process or `None` if it has yet to start

- **kwargs**

- **map_zero**

- **name**

- **pid**

    Return identifier (PID) of process or `None` if it has yet to start

- **proc**

- **uid_map**

##### Methods
- **__init__** (self, target_pid, target, args=(), kwargs={}, proc='/proc', *pargs, **pkwargs)

    Set new namespaces and execute Process.__init__
  
    Set self.setns as target with necessary args and kwargs.  
Then execute Process.__init__ with updated parameters.

      
Args:  

    * target_pid (str or int): pid of target process,
used for executing setns

    * target (python function): python function
for executing

    * args (list): args for target,
default is ()

    * kwargs (dict): kwargs for target,
default is {}

    * proc (str): root directory of proc fs,
default is '/proc'

    * *pargs (list): arguments for Container.__init__

    * **pkwargs (dict): arguments for Container.__init__
  
    In args or kwargs expected one or many of
many keys for setns:  
'all', 'ipc', 'newipc', 'mnt', 'newns',
'net', 'newnet', 'pid', 'newpid',
'user', 'newuser', 'uts', 'newuts'.  
If no one of them submitted 'all' will
be used.

- **is_alive** (self)

    Return whether process is alive

- **join** (self, timeout=None)

    Wait until child process terminates

- **run** (self)

    Method to be run in sub-process; can be overridden in sub-class

- **setns** (self, target_pid, target, args=(), kwargs={}, nspaces=[], proc='/proc')

    Change namespaces and execute target.
  
    Args:  

    * path (str): path to chroot new root

    * target (python function): python function
for executing after chroot

    * args (list): args for target,
default is ()

    * kwargs (dict): kwargs for target,
default is {}

    * nspaces (list): list of namespaces for setns

    * proc (str): root directory of proc fs,
default is '/proc'

    * all (bool): set all 6 namespaces,
default is False

    * newuts, uts (bool or str): enter uts namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

    * newipc, ipc (bool or str): enter ipc namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

    * newuser, user (bool or str): enter user namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

    * newpid, pid (bool or str): enter pid namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

    * newnet, net (bool or str): enter net namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

    * newns, mnt (bool or str): enter mount namespace,  
True or namespace file expected,
does not enter ns enev with 'all' arg if False,
default is None

- **start** (self)

    Start child process

- **terminate** (self)

    Terminate process; sends SIGTERM signal or uses TerminateProcess()
