from __future__ import absolute_import
try:
    from .base import from_dict, to_dict
    from .serialisable import Serialisable
    from .serialiser import Serialiser
    import msgpack as serialiser
    from msgpack import *


    def load(*args, **kwargs):
        kwargs['object_hook'] = from_dict
        return serialiser.load(*args, **kwargs)


    def loads(*args, **kwargs):
        kwargs['object_hook'] = from_dict
        return serialiser.loads(*args, **kwargs)


    def dump(*args, **kwargs):
        kwargs['default'] = to_dict
        return serialiser.dump(*args, **kwargs)


    def dumps(*args, **kwargs):
        kwargs['default'] = to_dict
        return serialiser.dumps(*args, **kwargs)
except:
    pass
