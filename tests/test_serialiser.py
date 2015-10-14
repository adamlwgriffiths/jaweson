import unittest
import numpy as np
import jaweson
from jaweson import json, msgpack


class TestSerialiser(unittest.TestCase):
    def test_int(self):
        obj = 1
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, int)
        assert obj == jobj
        assert isinstance(jobj, int)

    def test_float(self):
        obj = 3.14159
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, float)
        assert obj == jobj
        assert isinstance(jobj, float)

    def test_str(self):
        obj = "abc"
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, (str, unicode))
        assert obj == jobj
        assert isinstance(jobj, (str, unicode))

    def test_set(self):
        obj = set([1, 2, 3])
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, set)
        assert obj == jobj
        assert isinstance(jobj, set)

    def test_list(self):
        obj = [1, 2, 3]
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, list)
        assert obj == jobj
        assert isinstance(jobj, list)

    def test_dict(self):
        obj = {'a': 1, 'b': 2, 'c': 3}
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, dict)
        assert obj == jobj
        assert isinstance(jobj, dict)

    def test_dict_int_keys(self):
        obj = {1: 1, 2: 2, 3: 3}
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, dict)
        # we cannot test this as JSON will convert int keys to strings
        #assert obj == jobj
        assert isinstance(jobj, dict)

    def test_complex(self):
        obj = complex(123)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj == mobj
        assert isinstance(mobj, complex)
        assert obj == jobj
        assert isinstance(jobj, complex)

    def test_ndarray(self):
        obj = np.array([1, 2, 3], dtype=np.float32)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.dtype == np.float32
        assert (obj == mobj).all()
        assert obj.dtype == mobj.dtype
        assert isinstance(mobj, np.ndarray)
        assert (obj == jobj).all()
        assert obj.dtype == jobj.dtype
        assert isinstance(jobj, np.ndarray)

    def test_npgeneric(self):
        obj = np.float32(1)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.dtype == np.float32
        assert obj == mobj
        assert obj.dtype == mobj.dtype
        assert isinstance(mobj, np.generic)
        assert obj == jobj
        assert obj.dtype == jobj.dtype
        assert isinstance(jobj, np.generic)

    def test_serialisable(self):
        class SerialisableObject(jaweson.Serialisable):
            def __init__(self):
                self.a = 1

        obj = SerialisableObject()
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 1
        assert obj.a == mobj.a
        assert obj.a == jobj.a

    def test_serialisable_constructor(self):
        class SerialisableConstructorObject(jaweson.Serialisable):
            def __init__(self, a):
                self.a = a

        obj = SerialisableConstructorObject(2)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 2
        assert obj.a == mobj.a
        assert obj.a == jobj.a

    def test_class_variable(self):
        class ClassVariableObject(jaweson.Serialisable):
            a = 1

        obj = ClassVariableObject()
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 1
        assert obj.a == mobj.a
        assert obj.a == jobj.a

        assert '_Serialisable__a' not in json.dumps(obj)

    def test_modified_class_variable(self):
        class ClassVariableOverrideObject(jaweson.Serialisable):
            a = 1

            def __init__(self):
                self.a = 2

        obj = ClassVariableOverrideObject()
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 2
        assert obj.a == mobj.a
        assert obj.a == jobj.a

        assert '_Serialisable__a' not in json.dumps(obj)
        assert 'a' in json.dumps(obj)

    def test_non_serialisable(self):
        class NonSerialisableObject(object):
            def __init__(self):
                self.a = 1

        obj = NonSerialisableObject()

        with self.assertRaises(TypeError):
            msgpack.dumps(obj)

        with self.assertRaises(TypeError):
            json.dumps(obj)

    def test_custom_serialiser(self):
        class CustomSerialiserObject(jaweson.Serialisable):
            @classmethod
            def to_json(cls, obj):
                return {'c': obj.a, 'd': obj.b}

            @classmethod
            def from_json(cls, obj):
                return cls(int(obj['c']), int(obj['d']))

            def __init__(self, a, b):
                self.a = a
                self.b = b

        obj = CustomSerialiserObject(1, 2)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 1
        assert obj.b == 2
        assert obj.a == mobj.a
        assert obj.b == mobj.b
        assert obj.a == jobj.a
        assert obj.b == jobj.b

    def test_dodgy_constructor(self):
        class DodgyConstructor(jaweson.Serialisable):
            def __init__(self, a, b):
                # flip the order
                self.a = b
                self.b = a

        obj = DodgyConstructor(1, 2)
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.a == 2
        assert obj.b == 1
        assert obj.a == mobj.a
        assert obj.b == mobj.b
        assert obj.a == jobj.a
        assert obj.b == jobj.b

    def test_hierarchy(self):
        class Node(jaweson.Serialisable):
            def __init__(self, name, child=None):
                self.name = name
                self.child = child

        obj = Node(1, Node(2, Node(3)))
        mobj = msgpack.loads(msgpack.dumps(obj))
        jobj = json.loads(json.dumps(obj))

        assert obj.name == 1
        assert obj.child.name == 2
        assert obj.child.child.name == 3
        assert isinstance(obj, Node)

        assert obj.name == mobj.name
        assert obj.child.name == mobj.child.name
        assert obj.child.child.name == mobj.child.child.name
        assert obj.name == jobj.name
        assert obj.child.name == jobj.child.name
        assert obj.child.child.name == jobj.child.child.name


if __name__ == '__main__':
    unittest.main()
