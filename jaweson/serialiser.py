from __future__ import absolute_import
import numpy as np
import base64


# TODO: add date/time/datetime serialiser

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


class NumpySerialiser(Serialiser):
    python_types = (np.ndarray, np.generic)
    serialised_types = ('ndarray', 'npgeneric')

    def to_dict(self, obj):
        if isinstance(obj, np.ndarray):
            return {
                '__type__': 'ndarray',
                'data': base64.b64encode(obj.tostring()),
                'dtype': obj.dtype.str,
                'shape': obj.shape,
            }
        elif isinstance(obj, (np.bool_, np.number)):
            return {
                '__type__': 'npgeneric',
                'data': base64.b64encode(obj.tostring()),
                'dtype': obj.dtype.str,
            }

        return super(NumpySerialiser, self).to_dict(obj)

    def from_dict(self, jobj):
        obj = np.fromstring(
            base64.b64decode(jobj['data']),
            dtype=np.dtype(jobj['dtype'])
        )
        if jobj.get('__type__') == 'ndarray':
            return obj.reshape(jobj['shape'])
        if jobj.get('__type__') == 'npgeneric':
            return obj[0]

        return super(NumpySerialiser, self).from_dict(jobj)


class PythonTypeSerialiser(Serialiser):
    python_types = (set, tuple, complex)
    serialised_types = ('set', 'tuple', 'complex')

    def to_dict(self, obj):
        if isinstance(obj, set):
            return {
                '__type__': 'set',
                'data': list(obj),
            }
        if isinstance(obj, tuple):
            return {
                '__type__': 'tuple',
                'data': list(obj)
            }
        if isinstance(obj, complex):
            return {
                '__type__': 'complex',
                'data': obj.__repr__()
            }

        return super(PythonTypeSerialiser, self).to_dict(obj)

    def from_dict(self, jobj):
        if jobj.get('__type__') == 'set':
            return set(jobj['data'])
        if jobj.get('__type__') == 'tuple':
            return tuple(jobj['data'])
        if jobj.get('__type__') == 'complex':
            return complex(jobj['data'])

        return super(PythonTypeSerialiser, self).from_dict(jobj)
