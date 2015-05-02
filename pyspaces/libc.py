#!/usr/bin/env python
# coding=utf-8


from ctypes import *


libc = CDLL("libc.so.6", use_errno=True)
"""Import libc.so.6 as libc"""
