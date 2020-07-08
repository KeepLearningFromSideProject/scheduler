#!/usr/local/env python3
import sys
from subprocess import Popen, PIPE
from urllib.parse import quote_plus, unquote_plus

def solver(code):
    execute_command = ["python3", "-c", code]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

    # wait for the process to terminate
    # or use p.wait() to wait
    out, err = p.communicate()
    print(out.decode("utf-8"), end='')

def main():
    code = unquote_plus(sys.argv[1])
    solver(code)

if __name__ == "__main__":
    main()
