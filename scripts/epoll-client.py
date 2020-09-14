#!/usr/bin/env python3
import socket
import os
import sys
import glob

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 8888)
try:
    sock.connect(server_address)
except socket.error as error:
    sys.exit(1)

sock.send(str.encode('hello'))
response = sock.recv(4096)
print(response)
