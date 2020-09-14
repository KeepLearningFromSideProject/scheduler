#!/usr/bin/env python3
import socket
import os
import sys
import glob

tmp_files = glob.glob('/tmp/*unixsocket')

if len(tmp_files) == 0:
    sys.exit(1)
UNIX_SOCKET_ADDRESS = '{}/socket9527'.format(tmp_files[0])
print(UNIX_SOCKET_ADDRESS)

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    sock.connect(UNIX_SOCKET_ADDRESS)
except socket.error as error:
    sys.exit(1)

sock.send(str.encode('hello'))
response = sock.recv(4096)
print(response)
