#!/usr/bin/env python3
import os
from os.path import abspath
import sys
import socket
import tempfile
from contextlib import contextmanager
import shutil

'''
# complem implementation
# 
import shutil
import tempfile

class TemporaryDirectory(object):
    """Context manager for tempfile.mkdtemp() so it's usable with "with" statement."""
    def __enter__(self):
        self.name = tempfile.mkdtemp()
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)
'''


# mkdtemp: create unique temporary directroy
# mkstemp: create unique  

@contextmanager
def CustomTemporaryDirectory():
    name = tempfile.mkdtemp('_unixsocket')
    try:
        yield name
    finally:
        shutil.rmtree(name)



with CustomTemporaryDirectory() as tmp_dir:
    print(tmp_dir)
    with open(tmp_dir+'/socket9527', 'w') as f:
        print('create unix socket file successfully')
    UNIX_SOCKET_ADDRESS = '{}/socket9527'.format(tmp_dir)
    print(UNIX_SOCKET_ADDRESS)

    try:
        os.unlink(UNIX_SOCKET_ADDRESS)
    except OSError:
        if os.path.exists(UNIX_SOCKET_ADDRESS):
            raise
    
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(UNIX_SOCKET_ADDRESS)
    sock.listen(1)
    
    while True:
        connection, client_address = sock.accept()
        try:
            while True:
                data = connection.recv(1000)
                if data:
                    print(data)
                    connection.send(str.encode('hello'))
                else:
                    break
        finally:
            connection.close()
