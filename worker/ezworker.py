#!/usr/local/env python3
import sys
from subprocess import Popen, PIPE

def translator(code, args):
    pass

def solver(code, args):
    execute_command = ["python3", "-c", code, args]
    p = Popen(execute_command, stdout=PIPE, stderr=PIPE)

    # wait for the process to terminate
    # or use p.wait() to wait
    out, err = p.communicate()
    print(out)

def main():
    code = sys.argv[1]
    args = sys.argv[2]

    translator(code, args)
    solver(code, args)

if __name__ == "__main__":
    main()