"""Provides Object -> JSON -> Object serialisation functionality.

This code is designed to avoid any `eval` calls which could be
exploited, if the database were compromised, with malicious code.

To avoid calling `eval` on the class type, classes must be registered
with the `register_type` function.

Note: A badly written class could still parse internal data using eval.
"""
from __future__ import absolute_import
from .base import to_dict, from_dict
from .serialisable import Serialisable
from .serialiser import Serialiser
from .serialisers import base, datetime, numpy

from .version import __version__
