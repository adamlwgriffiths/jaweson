from __future__ import absolute_import

try:
    from ..serialiser import Serialiser
    import base64
    import numpy as np

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
except:
    # no numpy support
    pass
