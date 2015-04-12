#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from __future__ import with_statement

__author__ = 'Filipp Frizzy'
__credits__ = ["Filipp Frizzy"]
__license__ = "MIT"
__version__ = ""
__maintainer__ = "Filipp Frizzy"
__email__ = "filipp.s.frizzy@gmail.com"
__status__ = "Development"

import os
import sys
import pytest
import subprocess


path_to_module = os.path.abspath(os.path.join(
                   os.path.dirname(os.path.realpath(__file__)),
                   '..'))
sys.path.insert(0, path_to_module) 
