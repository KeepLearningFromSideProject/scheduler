#!/usr/bin/env python3
import uuid

class Task:
    def __init__(self, hostname, typename, content=None):
        self.uuid = uuid.uuid1()
        self.host = hostname
        self.status = "pending"
        self.type = typename
        self.content = content


