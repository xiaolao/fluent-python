# coding: utf-8
__author__ = "ceq"

import collections
from math import hypot
from array import array
from random import random
import time
import numpy
import abc
import types
import codecs


Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._card = [Card(rank, suit) for suit in self.suits
                                       for rank in self.ranks]

    def __len__(self):
        return len(self._card)

    def __getitem__(self, position):
        return self._card[position]


spades_value = dict(spades=0, diamonds=1, clubs=2, hearts=3)


def sort_key(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(spades_value) + spades_value[card.suit]


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Vector(%r, %r)' % (self.x, self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)


def array_test():
    t1 = time.time()
    floats = array('d', (random() for i in range(10 ** 7)))
    t2 = time.time()
    print(t2 - t1)
    fp = open('floats.bin', 'wb')
    floats.tofile(fp)
    fp.close()
    t3 = time.time()
    print(t3 - t2)
    floats2 = array('d')
    fp = open('floats.bin', 'rb')
    floats2.fromfile(fp, 10 ** 7)
    fp.close()
    t4 = time.time()
    print(t4 - t3)
