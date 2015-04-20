Module pyspaces.cloning
-----------------------

Variables
---------
- **CLONE_CHILD_CLEARTID**

    clear the TID in the child

- **CLONE_CHILD_SETTID**

    set the TID in the child

- **CLONE_DETACHED**

    Unused, ignored

- **CLONE_FILES**

    set if open files shared between processes

- **CLONE_FS**

    set if fs info shared between processes

- **CLONE_IO**

    Clone io context

- **CLONE_NEWIPC**

    New ipc namespace

- **CLONE_NEWNET**

    New network namespace

- **CLONE_NEWNS**

    New mount namespace group

- **CLONE_NEWPID**

    New pid namespace

- **CLONE_NEWUSER**

    New user namespace

- **CLONE_NEWUTS**

    New utsname namespace

- **CLONE_PARENT**

    set if we want to have the same parent as the cloner

- **CLONE_PARENT_SETTID**

    set the TID in the parent

- **CLONE_PTRACE**

    set if we want to let tracing continue on the child too

- **CLONE_SETTLS**

    create a new TLS for the child

- **CLONE_SIGHAND**

    set if signal handlers and blocked signals shared

- **CLONE_SYSVSEM**

    share system V SEM_UNDO semantics

- **CLONE_THREAD**

    Same thread group?

- **CLONE_UNTRACED**

    set if the tracing process can't force CLONE_PTRACE on this clone

- **CLONE_VFORK**

    set if the parent wants the child to wake it up on mm_release

- **CLONE_VM**

    set if VM shared between processes

- **DEFAULT_MODE**

- **RTLD_GLOBAL**

- **RTLD_LOCAL**

- **STACK_SIZE**

    STACK_SIZE (1024 * 1024)

Classes
-------
#### Clone 
Inheritance from `multiprocessing.forking.Popen`.
  
We define a Popen class similar to the one from subprocess, but
whose constructor takes a process object as its argument.

##### Ancestors (in MRO)
- pyspaces.cloning.Clone

- multiprocessing.forking.Popen

- __builtin__.object

##### Static methods
- **thread_is_spawning** ()

##### Instance variables
- **pid**

- **pipe_fd**

- **process_obj**

- **returncode**

- **sentinel**

##### Methods
- **__init__** (self, process_obj)

    Execute linux clone.
  
    Create a child process in new namespace(s);
allow UID and GID mappings to be specified when
creating a user namespace.

- **child** (self)

    Start function for cloned child.
  
    Wait until the parent has updated the UID and GID mappings.  
See the comment in main(). We wait for end of file on a
pipe that will be closed by the parent process once it has
updated the mappings.

- **poll** (self, flag=1)

- **terminate** (self)

- **update_map** (self, mapping, map_file)

    Update the mapping file 'map_file', with the value provided in
'mapping', a string that defines a UID or GID mapping. A UID or  
GID mapping consists of one or more newline-delimited records
of the form:  
  
    ID_inside-ns    ID-outside-ns   length
  
    Requiring the user to supply a string that contains newlines is
of course inconvenient for command-line use. Thus, we permit the
use of commas to delimit records in this string, and replace them
with newlines before writing the string to the file.

- **wait** (self, timeout=None)
