from flask import Flask, request, jsonify
from subprocess import Popen, PIPE
from os.path import abspath, expanduser
import requests
import time
import json
import sys

app = Flask(__name__)

@app.route("/execute-file/<code>")
def execute_file(code):
    print('execute')
    print(code)
    task = {}

    PYTHON = 'python3'
    # EXECUTE_SCRIPT = self.model_script_dir + '/train_mnist.py'
    EXECUTE_SCRIPT = code
    execute_command = [PYTHON, "-c", EXECUTE_SCRIPT]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

    # wait for the process to terminate
    # or use p.wait() to wait
    out, err = p.communicate()

    return out

def main():
    global app

    # launch RESTful server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()