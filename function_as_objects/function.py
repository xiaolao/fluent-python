# coding: utf-8
__author__ = "Jeffrey Chen"


import inspect
from collections import namedtuple
from functools import reduce


def tag(name, *content, cls=None, **attrs):
    if cls is not None:
        attrs["class"] = cls
    if attrs:
        attrs_str = ' '.join('%s="%s"' % (key, value)
                             for key, value in sorted(attrs.items()))
    else:
        attrs_str = ''
    if content:
        return '\n'.join('<%s %s>%s</%s>' % (name, attrs_str, c, name)
                         for c in content)
    else:
        return '<%s\>' % name


def clip(text: str, max_len: 'int > 10'=80) -> str:
    """
    return text clipped.
    """
    end = None
    if len(text) < max_len:
        end = len(text)
    else:
        space_before = text.find(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.find(' ', max_len)
            if space_before >= 0:
                end = space_after
    if end is None:
        end = max_len
    return text[:end].rstrip()


Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
    u"""
    一类物品
    """

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    @property
    def total(self):
        return self.quantity * self.price


class Order:
    """
    订单
    """

    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    @property
    def total(self):
        if not hasattr(self, '_total'):
            self._total = sum([item.total for item in self.cart])
        return self._total

    @property
    def due(self):
        if self.promotion is None:
            return self.total
        else:
            return self.total - self.promotion(self)

    def __repr__(self):
        fmt = '<Order totla: {:.2f}, due: {:.2f}>'
        return fmt.format(self.total, self.due)


promo = []


def register(func):
    promo.append(func)
    return func


@register
def fidelity_promo(order):
    return order.total * .05 if order.customer.fidelity >= 1000 else 0


@register
def bulk_item_promo(order):
    return sum([item.total * .1 for item in order.cart if item.quantity >= 20])


@register
def large_order_promo(order):
    distinct_item = {item.product for item in order.cart}
    if len(distinct_item) >= 10:
        return order.total * .07
    return 0


def best_promo(order):
    return max(p(order) for p in promo)


# callable object
class Average:

    def __init__(self):
        self.seris = []

    def __call__(self, price):
        return sum(self.seris)/len(self.seris)


# closures
def make_average():
    seris = []

    def average(price):
        seris.append(price)
        return sum(seris)/len(seris)
