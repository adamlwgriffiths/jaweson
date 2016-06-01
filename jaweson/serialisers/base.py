from __future__ import absolute_import
from ..serialiser import Serialiser

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
