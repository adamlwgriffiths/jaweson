=======
JAWESON
=======

JSON + Awesome serialisation = JAWESON

JAWESON provides a modular serialisation framework for JSON parsing.
The functions themselves are not dependent on JSON and can be repurposed to
any serialisation format that handles dicts, lists, strings, ints and floats.

JAWESON avoids using pickle to avoid potential security issues. Should your pickle
store (database, s3, etc) become compromised, your system could be tricked into
running malicious code.

Avoiding pickle is not without a cost, and that is the need to provide support for
non-JSON friendly types.

Example::

    import jaweson as json
    import numpy as np

    a = [1,2,3]
    j = json.dumps(a)
    print j
    >>> [1, 2, 3]
    b = json.loads(j)
    assert b == a

    a = np.array([1,2,3], dtype=np.float32)
    j = json.dumps(a)
    print j
    >>> {"data": "AACAPwAAAEAAAEBA", "shape": [3], "__type__": "ndarray", "dtype": "<f4"}
    b = json.loads(j)
    assert (b == a).all()

    class Test(json.Serialisable):
        def __init__(self):
            self.a = 1

        def modify(self):
            self.a = 2

    a = Test()
    j = json.dumps(a)
    print j
    >>> {"a": 1, "__type__": "serialisable", "__class__": "Test"}
    b = json.loads(j)
    assert b.a is 1

    a.modify()
    j = json.dumps(a)
    print j
    >>> {"a": 2, "__type__": "serialisable", "__class__": "Test"}
    b = json.loads(j)

    assert b.a is 2


Out-of-the-box Support
======================

JAWESON supports serialisation of the following types out-of-the-box:

* default JSON types (dict, list, string, int, float, null)
* set
* tuple
* np.ndarray
* np.generic
* jsom.Serialisable



Object Serialisation
====================

JAWESON supports object serialisation through the use of a jsom.Serialisable
base class.

This class provides functionality to:

* Automatically register itself for creation.
* Automatically serialise values.
* Automatically construct and deserialise values.


Custom parsing can be provided by overloading the jaweson.Serialisable
to_json and from_json class methods.::

    class MyObject(jaweson.Serialisable):
        @classmethod
        def to_json(cls, obj):
            data = super(MyObject, cls).to_json(obj)
            data['my_value'] = obj.my_other_value

        @classmethod
        def from_json(cls, jobj):
            obj = super(MyObject, cls).from_json(jobj)
            obj.my_other_value = jobj['my_value']


Custom Serialisers
==================

Support for new seralisers can be added by inheriting from the jaweson.Serialiser class.

Classes are automatically registered with the jaweson serialiser when parsed.

The following code is for the built-in Python type serialiser::

    from jaweson import Serialiser

    class PythonTypeSerialiser(Serialiser):
        python_types = (set, tuple, complex)
        serialised_types = ('set', 'tuple', 'complex')

        def to_json(self, obj):
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

            return super(PythonTypeSerialiser, self).to_json(obj)

        def from_json(self, jobj):
            obj = np.fromstring(
                base64.b64decode(jobj['data']),
                dtype=np.dtype(jobj['dtype'])
            )
            if jobj.get('__type__') == 'set':
                return set(obj['data'])
            if jobj.get('__type__') == 'tuple':
                return tuple(obj['data'])
            if jobj.get('__type__') == 'complex':
                return complex(obj['data'])

            return super(PythonTypeSerialiser, self).from_json(jobj)


Gotchas
=======

Constructors that modify incoming data can be a problem. Ensure you only
use simple constructors::

    import jaweson as json

    class BadClass(json.Serialisable):
        def __init__(self, a):
            self.a = a * 2

    a = BadClass(1)
    j = json.dumps(a)
    print a.a
    >>> 2
    b = json.loads(j)
    print b.a
    >>> 4


Having multiple classes with the same name defined will cause the de-serialiser
to become confused and fail.


Data format
===========


JAWESON stores complex objects in the following structure::

    {
        '__type__': '<type name>',
        <other fields>
    }


JAWESON implements the following serialisation formats.

numpy.ndarray::

    {
        '__type__': 'ndarray',
        'data': '<base 64 encoded data>',
        'dtype': '<numpy dtype>',
        'shape': [<shape>,],
    }

numpy.generic::

    {
        '__type__': 'ndarray',
        'data': '<base 64 encoded data>',
        'dtype': '<numpy dtype>',
    }

set::

    {
        '__type__': 'set',
        'data': [<set>],
    }

tuple::

    {
        '__type__': 'tuple',
        'data': [<tuple>],
    }

complex::

    {
        '__type__': 'complex',
        'data': '<base 64 encoded data>',
    }

jaweson.Serialisable::

    {
        '__type__': 'serialisable',
        '__class__': '<class name>',

    }


TODO
====

* datetime serialisation

