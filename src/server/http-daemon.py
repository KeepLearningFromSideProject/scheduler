#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template
from subprocess import Popen, PIPE
from os.path import abspath, expanduser
import requests
import time
import json
import sys
from urllib.parse import quote_plus, unquote_plus
import socket
import os

app = Flask(__name__)
server_address = ("127.0.0.1", 8888)

@app.route("/execute")
def execute():
    code = request.args.get('code')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
        print("client connect successful")
    except socket.error as error:
        sys.exit(1)
    
    #execute_command = ["python3", "../worker/ezworker.py", code]
    out ='hello'
    return out

@app.route("/")
def index():
    return render_template("index.html")

def main():
    global app

    # launch RESTful server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
