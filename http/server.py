#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template
from subprocess import Popen, PIPE
from os.path import abspath, expanduser
import requests
import time
import json
import sys

app = Flask(__name__)

@app.route("/execute")
def execute():
    code = request.args.get('code')
    args = request.args.get('args')

    PYTHON = 'python3'
    EXECUTE_SCRIPT = code
    EXECUTE_ARGS = args
    execute_command = [PYTHON, "-c", EXECUTE_SCRIPT, EXECUTE_ARGS]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

    # wait for the process to terminate
    # or use p.wait() to wait
    out, err = p.communicate()
    print(out)

    return out


@app.route("/execute-json")
def executejson():
    code = request.args.get('code')
    args = request.args.get('args')

    PYTHON = 'python3'
    EXECUTE_SCRIPT = code
    EXECUTE_ARGS = args
    execute_command = [PYTHON, "-c", EXECUTE_SCRIPT, EXECUTE_ARGS]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

    # wait for the process to terminate
    # or use p.wait() to wait
    out, err = p.communicate()
    print(out)

    return jsonify(out)

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
