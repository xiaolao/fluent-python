# coding: utf-8
__author__ = 'ceq'

import abc
import pyspider
from datetime import datetime

# Why declare virtual subclasses!

isinstance([], (list, tuple))


class MySequence(object):
    __metaclass__ = abc.ABCMeta


MySequence.register(list)
MySequence.register(tuple)


# __subclasshook__  duck-typing


class AbstractDuck(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def __subclasshook__(cls, other):
        quack = getattr(other, 'quack', None)
        if callable(quack):
            return True
        return NotImplemented


class Duck(object):
    def quack():
        pass


class NotDuck(object):
    quack = 'foo'


# Declaring a protocol

# using NotImplementError


class Task_1(object):
    def __init__(self):
        self.runs = []

    def run(self):
        start = datetime.now()
        result = self._run()
        end = datetime.now()
        self.runs.append({
            "start": start,
            "end": end,
            "result": result
        })
        return result

    def _run(self):
        raise NotImplementedError('_run method must be defined.')


# using metaclass
class TaskMeta(type):
    """A metaclass class that ensures the presence of a _run method on any
    non-abstract classes it create.
    """

    def __new__(cls, name, bases, attrs):
        if attrs.pop('abstract', False):
            return super(TaskMeta, cls).__new__(cls, name, bases, attrs)
        new_class = super(TaskMeta, cls).__new__(cls, name, bases, attrs)
        if not hasattr(new_class, '_run') or not callable(new_class._run):
            raise TypeError('Task subclass must define a _run method.')
        return new_class


class Task_2(object):
    __metaclass__ = TaskMeta
    abstract = True

    def __init__(self):
        self.runs = []

    def run(self):
        start = datetime.now()
        result = self._run()
        end = datetime.now()
        self.runs.append({
            "start": start,
            "end": end,
            "result": result
        })
        return result


# abstract base class decorator.

class Task_3(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.runs = []

    def run(self):
        start = datetime.now()
        result = self._run()
        end = datetime.now()
        self.runs.append({
            "start": start,
            "end": end,
            "result": result
        })
        return result

    @abc.abstractmethod
    def _run(self):
        pass


# abstract property
class AbstractClass(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def foo(self):
        pass
