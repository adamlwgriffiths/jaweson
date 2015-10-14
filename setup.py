#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


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
    platforms=['any'],
    #test_suite='tests',
    packages=['jaweson'],
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
