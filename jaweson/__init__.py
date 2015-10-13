"""Provides Object -> JSON -> Object serialisation functionality.

This code is designed to avoid any `eval` calls which could be
exploited, if the database were compromised, with malicious code.

To avoid calling `eval` on the class type, classes must be registered
with the `register_type` function.

Note: A badly written class could still parse internal data using eval.
"""

from . import serialisable
from . import serialiser
from .serialisable import Serialisable
from .serialiser import Serialiser
import json
from json import *


def to_dict(obj):
    s = serialiser.find_serialiser(obj)
    if s:
        return s.to_dict(obj)

    raise TypeError('Unable to serialise object of type {}'.format(type(obj)))


def from_dict(jobj):
    if '__type__' in jobj:
        s = serialiser.find_deserialiser(jobj['__type__'])
        if s:
            return s.from_dict(jobj)
    return jobj


def load(*args, **kwargs):
    kwargs['object_hook'] = from_dict
    return json.load(*args, **kwargs)


def loads(*args, **kwargs):
    kwargs['object_hook'] = from_dict
    return json.loads(*args, **kwargs)


def dump(*args, **kwargs):
    kwargs['default'] = to_dict
    return json.dump(*args, **kwargs)


def dumps(*args, **kwargs):
    kwargs['default'] = to_dict
    return json.dumps(*args, **kwargs)
