# coding: utf-8

import subprocess
import contextlib


class ContextManager(object):
    def __init__(self):
        self.entered = False

    def __enter__(self):
        self.entered = True
        return self

    def __exit__(self, exc_type, exc_instence, traceback):
        self.entered = False


# Excluding Subclasses
class ValueErrorSubclass(ValueError):
    pass


class HandleValueError(object):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_instence, traceback):
        if not exc_type:
            return
        if exc_type == ValueError:
            return True
        return False


# Attribute-Based Exception Handing
class ShellException(Exception):
    def __init__(self, code, stdout='', stderr=''):
        self.code = code
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return 'exit code %d - %s' % (self.code, self.stderr)


def run_command(command):
    proc = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.wait()
    stdout, stderr = proc.communicate()
    if proc.returncode > 0:
        raise ShellException(proc.returncode, stdout, stderr)
    return stdout


class AcceptableErrorCodes(object):
    """
    this context manager is to handle ShellException with certain code
    of error
    """
    def __init__(self, *error_codes):
        self.error_codes = error_codes

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_instence, traceback):
        if not exc_type:
            return True
        if not issubclass(exc_type, ShellException):
            return False
        return exc_instence.code in self.error_codes


@contextlib.contextmanager
def acceptable_error_codes(*codes):
    try:
        yield
    except ShellException as exc_instence:
        if exc_instence.code not in codes:
            raise

@contextlib.contextmanager
def LookingGlass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield "this is for test"
    sys.stdout.write = original_write
