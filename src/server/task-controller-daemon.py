#!/usr/bin/env python3

import select
import socket
import queue
from common import Task

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# reuse addr
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("127.0.0.1", 8888)
serversocket.bind(server_address)
serversocket.listen(100)
print("launch successfully" , server_address)
# non-block
serversocket.setblocking(False)

# epoll
timeout = 10
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
message_queues = {}
fd_to_socket = {serversocket.fileno():serversocket,}

while True:
    print("waiting......")
    events = epoll.poll(timeout)
    if not events:
        print("epoll timeout")
        continue
    print(len(events), " connections are waiting")

    for fd, event in events:
        socket = fd_to_socket[fd]
        if socket == serversocket:
            connection, address = serversocket.accept()
            print("new connection" , address)
            connection.setblocking(False)
            epoll.register(connection.fileno(), select.EPOLLIN)
            fd_to_socket[connection.fileno()] = connection
            message_queues[connection]  = queue.Queue()
        elif event & select.EPOLLHUP:
            print("client close")
            epoll.unregister(fd)
            fd_to_socket[fd].close()
            del fd_to_socket[fd]
        elif event & select.EPOLLIN:
            data = socket.recv()
            if data:
                print("get:" , data , "client" , socket.getpeername())
                data = json.loads(data)
                print(data)
                message_queues[socket].put(data)
                epoll.modify(fd, select.EPOLLOUT)
        elif event & select.EPOLLOUT:
            try:
                msg = message_queues[socket].get_nowait()
            except queue.Empty:
                print(socket.getpeername() , " queue empty")
                epoll.modify(fd, select.EPOLLIN)
        else:
            print("send" , data , "client:" , socket.getpeername())
            socket.send(msg)

# unregister
epoll.unregister(serversocket.fileno())
epoll.close()
serversocket.close()



