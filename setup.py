#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('jsome/version.py', 'r') as f:
    exec(f.read())

setup(
    name='jsome',
    version=__version__,
    description='Powerful serialisation for JSON, without the risk',
    license='BSD',
    author='Adam Griffiths',
    url='https://github.com/adamlwgriffiths/jsome',
    install_requires=['json'],
    platforms=['any'],
    #test_suite='tests',
    packages=['jsome'],
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
