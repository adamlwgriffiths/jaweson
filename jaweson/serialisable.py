from __future__ import absolute_import
from .serialiser import Serialiser


_types = {}


def register_class(obj, clsname=None):
    global _types
    name = clsname or obj.__name__
    if name in _types:
        raise TypeError('A class with the name "{}" is already defined'.format(name))
    _types[name] = obj


class SerialisableMetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        '''Automatically registers Serialisable subclasses at class definition time.
        '''
        newclass = super(SerialisableMetaClass, cls).__new__(cls, clsname, bases, attrs)
        serialised_cls = getattr(newclass, '_{}__classname'.format(clsname), None)
        register_class(newclass, serialised_cls)
        return newclass


class Serialisable(object):
    __metaclass__ = SerialisableMetaClass

    __classname = None

    # stores a list of class attributes which should not be serialised
    __whitelist = []
    __blacklist = []

    @classmethod
    def serialisable(cls, key, obj):
        '''Determines what can be serialised and what shouldn't
        '''
        # ignore class method names
        if key.startswith('_Serialisable'.format(cls.__name__)):
            return False
        if key in obj.__whitelist:
            return True
        # class variables will be prefixed with '_<cls.__name__>__variable'
        # so let's remove these too
        #if key.startswith('__'):
        if '__' in key:
            return False
        # ignore our own class variables
        #if key in ['_Serialisable__whitelist', '_Serialisable__blacklist']:
        #    return False
        if key in obj.__blacklist:
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
        that isn't prefixed with __, isn't in the blacklist, and isn't
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
            obj = cls.__new__(cls)
            blacklist = set(['__class__', '__type__'] + cls.__blacklist)
            for k in set(jobj.keys()) - blacklist:
                setattr(obj, k, jobj[k])

            return obj
        except Exception as e:
            raise TypeError('Failed to deserialise {}: {} - args: {}'.format(cls.__name__, str(e), kwargs))


class SerialisableSerialiser(Serialiser):
    python_types = (Serialisable,)
    serialised_types = ('serialisable',)

    def to_dict(self, obj):
        if isinstance(obj, Serialisable):
            cls = obj.__class__
            clsname = getattr(obj, '_{}__classname'.format(cls.__name__), None) or cls.__name__
            data = obj.to_dict(obj)
            data.update({
                '__type__': 'serialisable',
                '__class__': clsname,
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
