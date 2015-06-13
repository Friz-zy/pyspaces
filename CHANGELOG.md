## [Unreleased][unreleased]
### Added
- target, args, kwargs as clearly required arguments
- get, get_all functions into args_aliases.py
- processing of different types of values for uid_map and gid_map agrguments
- target_pid, proc, rootdir, workdir, daemonize, stdin, stdout, stderr arguments into Container.__init__
- runup, preup, nsenter, chroot, chdir, chtty, postup, exceptup, preexec, postexec, exceptexec functions into Container
- proc variable into Clone and Container
- setns now can take path to namespaces files as arguments

### Changed
- add rasing value error in setns
- processing of args and kwargs in Container.__init__
- Inject and Chroot classes now based on Container and deprecated

## 1.3.1 - 2015-05-26
### Fixed
- order of namespaces in args_aliases: it's important for setns! via src of nsenter
- docstrings
- readme

## 1.3 - 2015-05-15
### Added
- setns.py with setns context manager
- args_aliases.py with dicts of possible additional arguments for many cases
- Inject class and cli

### Fixed
- error handling with ctypes in cloning.py
- setns

## 1.2.4 - 2015-05-02
### Fixed
- docstrings
- error handling
- add multilicensing: now pyspaces under MIT or BSD or Apache 2.0
- up cli and example in readme

### Added
- 'all' argument into Container.__init__

## 1.2.3 - 2015-04-30
### Added
- link to python-nsenter in readme
- TODO into readme
- discuss and link to butter in readme
- additional argument 'all' in cli

### Changed
- add alisas 'mnt' for 'fs' option of cli execute
- update importing in process.py
- docstrings
- cli structure

## 1.2.2 - 2015-04-21
### Fixed
- readme for pypi

## 1.2 - 2015-04-21
## Added
- new class Chroot in process.py
- chroot option in cli

### Changed
- cli example in readme

### Fixed
- cli verbose mode

## 1.1.3 - 2015-04-20
### Removed
- click from requireds

### Changed
- cli version now used argparse instead of click

## Added
- pins in readme
- docs

## 1.1.2 - 2015-04-19
### Fixed
- pypi index and readme

## 1.1.1 - 2015-04-19
### Changed
- add md2rst with pyndoc into setup.py

## 1.1 - 2015-04-18
### Added
- add cli
- add click as requirement library

### Fixed
- example in readme
- import convention for libc

## 1.0.5 - 2015-04-18
### Added
- CHANGELOG.md

### Changed
- move ctypes and libc into libc.py

### Fixed
- Add self.sentinel into cloning.Clone for python3 compatibility

## 1.0 - 2015-04-16
### Changed
- README.md
- docstrings

### Added
- setup.py and [package on pypi](https://pypi.python.org/pypi?name=pyspaces&version=1.0&:action=display)
- tests files
- directories structure
- cloning.py and process.py as first working concept
- initial commit with necessary files

[unreleased](https://github.com/Friz-zy/pyspaces/compare/v1.3.1...HEAD)
[1.3-1.3.1](https://github.com/Friz-zy/pyspaces/compare/v1.3...v1.3.1)
[1.2.4-1.3](https://github.com/Friz-zy/pyspaces/compare/v1.2.4...v1.3)
[1.2.3-1.2.4](https://github.com/Friz-zy/pyspaces/compare/v1.2.3...v1.2.4)
[1.2.2-1.2.3](https://github.com/Friz-zy/pyspaces/compare/v1.2.2...v1.2.3)
[1.2-1.2.2](https://github.com/Friz-zy/pyspaces/compare/v1.2...v1.2.2)
[1.1.3-1.2](https://github.com/Friz-zy/pyspaces/compare/v1.1.3...v1.2)
[1.1.2-1.1.3](https://github.com/Friz-zy/pyspaces/compare/v1.1.2...v1.1.3)
[1.1.1-1.1.2](https://github.com/Friz-zy/pyspaces/compare/v1.1.1...v1.1.2)
[1.1-1.1.1](https://github.com/Friz-zy/pyspaces/compare/v1.1...v1.1.1)
[1.0.5-1.1](https://github.com/Friz-zy/pyspaces/compare/v1.0.5...v1.1)
[1.0-1.0.5](https://github.com/Friz-zy/pyspaces/compare/v1.0...v1.0.5)
