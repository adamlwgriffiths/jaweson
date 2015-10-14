
.. image:: https://gist.githubusercontent.com/adamlwgriffiths/1e239df99d8f3699ce2e/raw/4a1afbc8e863712b6cae1a4bfd28cc019e47c480/jaweson.png


=======
JAWESON
=======

.. image:: https://travis-ci.org/someones/jaweson.svg?branch=master
    :target: https://travis-ci.org/someones/jaweson

(JSON|MsgPack) + Awesome serialisation = JAWESON

JAWESON provides a modular de|serialisation framework.
The functions themselves are not dependent on any one framework and can be repurposed to
any serialisation format that handles dicts, lists, strings, ints and floats.

JAWESON provides the ability to automatically serialise objects with the
only change being an inherited jaweson.Serialisable class.

JAWESON avoids using pickle to avoid potential security issues. Should your pickle
store (database, s3, etc) become compromised, your system could be tricked into
running malicious code.

Avoiding pickle is not without a cost, and that is the need to provide support for
non-serialisation friendly types.

An example of using JAWESON to de|serialise JSON::

    from jaweson import json
    import numpy as np

    a = np.array([1,2,3], dtype=np.float32)
    j = json.dumps(a)
    print j
    >>> {"data": "AACAPwAAAEAAAEBA", "shape": [3], "__type__": "ndarray", "dtype": "<f4"}
    b = json.loads(j)
    (b == a).all()
    >>> True

    class Test(json.Serialisable):
        def __init__(self):
            self.a = 1

        def modify(self):
            self.a = 2

    a = Test()
    a.modify()
    j = json.dumps(a)
    print j
    >>> {"a": 2, "__type__": "serialisable", "__class__": "Test"}
    b = json.loads(j)

    b.a is 2
    >>> True


The same example will work with MsgPack if the import is changed from::

    from jaweson import json


To::

    from jaweson import msgpack as json


Out-of-the-box Support
======================

JAWESON supports serialisation of the following types out-of-the-box:

* default serialisable types (dict, list, string, int, float, null)
* set
* tuple
* np.ndarray
* np.generic
* jaweson.Serialisable
* JSON support
* MSGPack support


JSON Support
============

Import the JSON module from Jaweson::

    from jaweson import json
    json.dumps(set([1,2,3]))
    >>> {"data": [1, 2, 3], "__type__": "set"}


MSGPack Support
===============

Import the msgpack module from Jaweson::

    from jaweson import msgpack as json
    json.dumps(set([1,2,3]))
    >>> ��data��__type__�set


Automatic Object Serialisation
==============================

JAWESON supports object serialisation through the use of a jaweson.Serialisable
base class.

This class provides functionality to:

* Automatically register itself for creation.
* Automatically serialise values.
* Automatically construct and deserialise values.


For 99% of cases, you are not required to make any change to your class, except
to inherit from jaweson.Serialisable::


    from jaweson import json

    class MyObject(json.Serialisable):
        def __init__(self):
            self.a = 1

        def modify(self):
            self.a = 2

    a = MyObject()
    a.modify()
    j = json.dumps(a)
    print j
    >>> {"a": 2, "__type__": "serialisable", "__class__": "MyObject"}
    b = json.loads(j)
    b.a is 2
    >>> True


Should automatical de|serialisation not work, or require custom de|serialisation,
parsing can be overriden through the jaweson.Serialisable to_dict and from_dict
class methods::

    from jaweson import Serialisable

    class MyCustomSerialisableObject(Serialisable):
        @classmethod
        def to_dict(cls, obj):
            data = super(MyCustomSerialisableObject, cls).to_dict(obj)
            data['my_value'] = obj.my_other_value

        @classmethod
        def from_dict(cls, jobj):
            obj = super(MyCustomSerialisableObject, cls).from_dict(jobj)
            obj.my_other_value = jobj['my_value']


White|Blacklisting variables is achieved through the class variables __blacklist and __whitelist::

    from jaweson import Serialisable

    class BlacklistObject(Serialisable):
        __blacklist = ['dont_serialise']
        __whitelist = ['__im_required']

        def __init__(self):
            self.dont_serialise = 5
            self.__im_required = 10



Custom Serialisers
==================

Support for new seralisers can be added by inheriting from the jaweson.Serialiser class.

Classes are automatically registered with the jaweson serialiser when parsed.

The following code is for the built-in Python type serialiser::

    from jaweson import Serialiser

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
                return set(obj['data'])
            if jobj.get('__type__') == 'tuple':
                return tuple(obj['data'])
            if jobj.get('__type__') == 'complex':
                return complex(obj['data'])

            return super(PythonTypeSerialiser, self).from_dict(jobj)


Gotchas
=======

.. image:: https://gist.githubusercontent.com/adamlwgriffiths/1e239df99d8f3699ce2e/raw/cbea36c8e8ad2c2e53979d76f75c8cecec12a266/spagett.gif

Ensure you use unique class names
---------------------------------

Having multiple classes with the same name defined will cause the de-serialiser
to become confused and fail.


Serialisable does not serialise any variables with '__' in its name
-------------------------------------------------------------------

To avoid serialising internal data-structures, Serialisable derived objects
will not serialise variables with `__` in them by default.
This can be over-ridden by defining specific variables in the `__whitelist` list::

    class Obj(jaweson.Serialisable):
        __whitelist = ['__a']
        def __init__(self):
            self.__a = 1


Constructors are not called
---------------------------

If you define a constant in a class constructor::

    class Obj(jaweson.Serialisable):
        def __init__(self):
            self.a = 1


And later change the value::

    class Obj(jaweson.Serialisable):
        def __init__(self):
            self.a = 2


Variables serialised before the change will still have the value `a=1`.

To over-come this, over-ride the `from_dict` method to force the
variable to the new value::


    class Obj(jaweson.Serialisable):
        @classmethod
        def from_dict(cls, jobj):
            obj = super(Obj, cls).from_dict(jobj)
            obj.a = 2

        def __init__(self):
            self.a = 2


JSON does not support dict keys of type int
-------------------------------------------

JSON imposes a limitation that dictionary keys must be strings::

    import msgpack
    msgpack.loads(msgpack.dumps({1:1,2:2}))
    >>> {1: 1, 2: 2}
    import json
    json.loads(json.dumps({1:1,2:2}))
    >>> {u'1': 1, u'2': 2}


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


Authors
=======

* `Adam Griffiths <https://github.com/adamlwgriffiths>`_
