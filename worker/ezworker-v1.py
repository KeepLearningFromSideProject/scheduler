#!/usr/local/env python3
import sys
from subprocess import Popen, PIPE, check_output

def translator(code, args):
    pass

# How to catch exception output from Python subprocess.check_output()?
# https://stackoverflow.com/a/61676517
def _run_command(command):
    log.debug('Command: {}'.format(command))
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.stderr:
        raise subprocess.CalledProcessError(
                returncode = result.returncode,
                cmd = result.args,
                stderr = result.stderr
                )
    if result.stdout:
        log.debug("Command Result: {}".format(result.stdout.decode("utf-8")))
    return result

def solver(code, args):
    try:
        result = _run_command(
            "python3 -c {} {}"
            .format(code, args)
        )
        return result
    except subprocess.CalledProcessError as error:
        if "Connect Error" in error.stderr.decode("utf-8"):
            log.error("Connect Error" )
        return ""

class ErrorHandler:
    def __init__(self):
        pass
    def ordered_number(self):
        pass

def main():
    code = sys.argv[1]
    args = sys.argv[2]

    translator(code, args)
    result = solver(code, args)

if __name__ == "__main__":
    main()