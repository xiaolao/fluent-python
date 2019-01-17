from itertools import (
    count,
    cycle,
    islice,
    compress
)


def fibonacci():
    numbers = []
    while True:
        if len(numbers) < 2:
            numbers.append(1)
        else:
            numbers.append(sum(numbers))
            numbers.pop(0)
        yield numbers[-1]


def squares(cursor=1):
    while True:
        response = yield cursor ** 2
        if response:
            cursor = int(response)
        else:
            cursor += 1


class Fib(object):
    def __init__(self):
        self.prev = 0
        self.curr = 1

    def __iter__(self):
        return self

    def next(self):
        value = self.curr
        self.curr += self.prev
        self.prev = value
        return value


def fib():
    prev, curr = 0, 1
    while 1:
        yield curr
        prev, curr = curr, curr + prev
