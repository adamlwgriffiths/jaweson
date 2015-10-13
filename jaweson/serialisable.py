from __future__ import absolute_import
import inspect
from .serialiser import Serialiser


_types = {}


def register_class(obj):
    global _types
    name = obj.__name__
    if name in _types:
        raise TypeError('A class with the name "{}"" is already defined'.format(name))
    _types[name] = obj


class SerialisableMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        '''Automatically registers Serialisable subclasses at class definition time.
        '''
        newclass = super(SerialisableMetaClass, cls).__new__(cls, clsname, bases, attrs)
        register_class(newclass)  # here is your register function
        return newclass


class Serialisable(object):
    __metaclass__ = SerialisableMetaClass

    # stores a list of class attributes which should not be serialised
    _blacklist = []

    @classmethod
    def serialisable(cls, key, obj):
        '''Determines what can be serialised and what shouldn't
        '''
        if key.startswith('_'):
            return False
        if key in obj._blacklist:
            return False
        if callable(getattr(obj, key)):
            return False
        # check for properties
        if hasattr(obj.__class__, key):
            if isinstance(getattr(obj.__class__, key), property):
                return False
        return True

    @classmethod
    def to_dict(cls, obj):
        '''Serialises the object, by default serialises anything
        that isn't prefixed with _, isn't in the blacklist, and isn't
        callable.
        '''
        return {
            k: getattr(obj, k)
            for k in dir(obj)
            if cls.serialisable(k, obj)
        }
        #raise NotImplementedError('No to_dict for {}'.format(cls.__class__.__name__))

    @classmethod
    def from_dict(cls, jobj):
        '''Deserialises the object.
        Automatically inspects the object's __init__ function and
        extracts the parameters.
        Can be trivially over-written.
        '''
        try:
            signature = inspect.getargspec(cls.__init__)
            kwargs = {}
            for arg in signature.args:
                if arg in jobj:
                    kwargs[arg] = jobj[arg]

            obj = cls(**kwargs)

            # set any values that aren't passed via the constructor
            # also include the class blacklist in case it has changed
            # we don't want to deserialise newly blacklisted variables
            blacklist = set(['__class__', '__type__'] + cls._blacklist)
            for k in set(jobj.keys()) - set(kwargs.keys()) - blacklist:
                setattr(obj, k, jobj[k])

            # it would be preferable to use this method
            #obj = cls.__new__(cls, **jobj)

            return obj
        except Exception as e:
            raise TypeError('Failed to deserialise {}: {} - args: {}'.format(cls.__name__, str(e), kwargs))


class SerialisableSerialiser(Serialiser):
    python_types = (Serialisable,)
    serialised_types = ('serialisable',)

    def to_dict(self, obj):
        if isinstance(obj, Serialisable):
            cls_name = obj.__class__.__name__
            data = obj.to_dict(obj)
            data.update({
                '__type__': 'serialisable',
                '__class__': cls_name,
            })
            return data

        return super(SerialisableSerialiser, self).to_dict(obj)

    def from_dict(self, jobj):
        global _types

        if jobj.get('__type__') == 'serialisable':
            cls_name = jobj['__class__']
            if cls_name not in _types:
                raise NotImplementedError('No type registered for {}'.format(cls_name))

            cls = _types[cls_name]
            if not hasattr(cls, 'from_dict'):
                raise NotImplementedError('No from_dict classmethod for type {}'.format(cls_name))

            return cls.from_dict(jobj)

        return super(SerialisableSerialiser, self).from_dict(jobj)
