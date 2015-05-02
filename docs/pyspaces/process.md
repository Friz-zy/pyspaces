Module pyspaces.process
-----------------------

* This is part of [pyspaces](https://github.com/Friz-zy/pyspaces)
  

* License: MIT or BSD or Apache 2.0  
Copyright (c) 2014 Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>

Classes
-------
#### Chroot 
Class wrapper over `pyspaces.Container`.
  
Chroot objects represent activity that is run in a separate process
in new filesystem and user namespaces.
  
The class is analagous to `threading.Thread`.

##### Ancestors (in MRO)
- pyspaces.process.Chroot

- pyspaces.process.Container

- multiprocessing.process.Process

- __builtin__.object

##### Instance variables
- **authkey**

- **clone_flags**

- **daemon**

    Return whether process is a daemon

- **exitcode**

    Return exit code of process or `None` if it has yet to stop

- **gid_map**

- **ident**

    Return identifier (PID) of process or `None` if it has yet to start

- **map_zero**

- **name**

- **pid**

    Return identifier (PID) of process or `None` if it has yet to start

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

    * args (list): args for target

    * kwargs (dict): kwargs for target

    * *cargs (list): arguments for Container.__init__

    * **ckwargs (dict): arguments for Container.__init__

- **chroot** (self, path, target, args=(), kwargs={})

    Change root and execute target.
  
    Change root with os.chroot. Then execute
target with args and kwargs.
  
    Args:  

    * path (str): path to chroot new root

    * target (python function): python function
for executing after chroot

    * args (list): args for target

    * kwargs (dict): kwargs for target

- **is_alive** (self)

    Return whether process is alive

- **join** (self, timeout=None)

    Wait until child process terminates

- **run** (self)

    Method to be run in sub-process; can be overridden in sub-class

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

##### Instance variables
- **authkey**

- **clone_flags**

- **daemon**

    Return whether process is a daemon

- **exitcode**

    Return exit code of process or `None` if it has yet to stop

- **gid_map**

- **ident**

    Return identifier (PID) of process or `None` if it has yet to start

- **map_zero**

- **name**

- **pid**

    Return identifier (PID) of process or `None` if it has yet to start

- **uid_map**

##### Methods
- **__init__** (self, *args, **kwargs)

    Set clone flags and execute Process.__init__
  
    Args:  

    * *args (list): arguments for Process.__init__

    * **kwargs (dict): arguments for Process.__init__

    * flags (int): flags for clone, default is 0

    * uid_map (str): UID mapping for new namespace,
default is ""

    * gid_map (str): GID mapping for new namespace,
default is ""

    * map_zero (bool): Map user's UID and GID to 0
in user namespace, default is False

    * all (bool): set all 6 namespaces,
default is False

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

    * newns (bool): set CLONE_NEWNS flag,
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

    * newuts (bool): set CLONE_NEWUTS flag,
default is False

    * newipc (bool): set CLONE_NEWIPC flag,
default is False

    * newuser (bool): set CLONE_NEWUSER flag,
default is False

    * newpid (bool): set CLONE_NEWPID flag,
default is False

    * newnet (bool): set CLONE_NEWNET flag,
default is False

    * io (bool): set CLONE_IO flag,
default is False

- **is_alive** (self)

    Return whether process is alive

- **join** (self, timeout=None)

    Wait until child process terminates

- **run** (self)

    Method to be run in sub-process; can be overridden in sub-class

- **start** (self)

    Start child process

- **terminate** (self)

    Terminate process; sends SIGTERM signal or uses TerminateProcess()
