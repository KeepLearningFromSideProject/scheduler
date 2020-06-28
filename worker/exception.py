#!/usr/bin/env python3

import traceback
import sys
from sys import stderr, stdout

import inspect
import pprint

class NetworkException(Exception):
    def __init__(self, detail):
        print(detail, file=stdout)

class InternalException(Exception):
    def __init__(self):
        pass

frame = None

def level_c(detail):
    global frame
    frame = inspect.currentframe()
    raise NetworkException(detail)

def level_b():
    detail = ['hello']
    level_c(detail)

def level_a():
    level_b()    

if __name__ == '__main__':
    name = sys.argv[1]
    head = sys.argv[2]
    detail = ['ddd']
    try:
        raise NetworkException(detail)
    except NetworkException:
        tb = traceback.format_exc()
        print(tb)

    try:
        level_a()
    except NetworkException:
        print(frame.f_back)# next outer frame object (this frame caller)
        print(frame.f_builtins) # builtins namespace seen by this frame
        print(frame.f_code) # code object being executed in this frame
        print(frame.f_globals) # global namespace seen by this frame
        print(frame.f_lasti) # index of last attempted instruction in bytecode
        print(frame.f_lineno) # current line number in Python source code
        print(frame.f_locals) # local namespace seen by this frame
        print(frame.f_trace) # tracing function for this frame, or None
