from __future__ import absolute_import

_serialisers = set()


def register_serialiser(cls):
    global _serialisers

    _serialisers.add(cls())


def serialisers():
    return _serialisers


def find_serialiser(python_type):
    for s in _serialisers:
        for t in s.python_types:
            if isinstance(python_type, t):
                return s


def find_deserialiser(serialised_type):
    for s in _serialisers:
        if serialised_type in s.serialised_types:
            return s


class SerialiserMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        '''Automatically registers Serialiser subclasses at class definition time.
        '''
        newclass = super(SerialiserMetaClass, cls).__new__(cls, clsname, bases, attrs)
        register_serialiser(newclass)  # here is your register function
        return newclass


class Serialiser(object):
    __metaclass__ = SerialiserMetaClass

    python_types = tuple()
    serialised_types = tuple()

    def to_dict(self, obj):
        raise ValueError('Unknown data type: {}'.format(type(obj)))

    def from_dict(self, jobj):
        raise ValueError('Unknown data type: {}'.format(jobj))
