# coding: utf-8
__author__ = 'ceq'

import csv

from django import forms


def get_credentail_class(use_proxy=False, tfa=False):
    """Return a class representing a credential for the given services,
    with an attribute repsenting the expected keys.
    """
    if use_proxy:
        keys = ['service_name', 'email_address']
    else:
        keys = ['username', 'password']
        if tfa:
            keys.append(tfa)

    class Credential(object):
        excepted_keys = set(keys)

        def __init__(self, **kwargs):
            if self.excepted_keys != set(kwargs.keys()):
                raise ValueError('keys dont match.')
            for k ,v in kwargs.items():
                setattr(self, k, v)

    return Credential


class get_credentail_form_class(service):
    keys = []
    with open('creds.csv', 'r') as csvfile:
        for row in csv.reader(csvfile):
            if row[0] != service.lower():
                continue
            keys.append(row[1])

    attr = {}
    for key in keys:
        field_kw = {}
        if 'password' in key:
            field_kw['widget'] = forms.PasswordInput
        attr[key] = forms.CharField(**field_kw)
    metaclass = type(forms.From)
    return metaclass('CredentialForm', (forms.Form,), attrs)

