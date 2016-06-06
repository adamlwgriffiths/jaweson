#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    # fix for virtualbox builds
    import os
    del os.link
except:
    pass


with open('jaweson/version.py', 'r') as f:
    exec(f.read())

setup(
    name='jaweson',
    version=__version__,
    description='A safe, modular, format agnostic, serialiser. Provides support for JSON, MsgPack',
    license='BSD',
    author='Adam Griffiths',
    url='https://github.com/someones/jaweson',
    install_requires=[],
    tests_require=['numpy', 'python-dateutil', 'pytz', 'msgpack-python'],
    extras_require={
        'numpy': ['numpy'],
        'datetime': ['python-dateutil', 'pytz'],
        'msgpack': ['msgpack-python'],
    },
    platforms=['any'],
    test_suite='tests',
    packages=['jaweson'],
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
