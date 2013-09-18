# -*- coding: utf-8 -*-
# Copyright (c) 2013, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.

"""
The raw API to OpenGL ES 2.0. There are multiple implementations of this API,
available as submodules of this module. This module is a copy of one of these
submodule implementations.
"""

# NOTE: modules in this package that start with one underscore are autogenerated

from __future__ import print_function, division, absolute_import

import vispy


class _GL_ENUM(int):
    """ Type to represent OpenGL constants.
    """
    def __new__(cls, name, value):
        base = int.__new__(cls, value)
        base.name = name
        return base
    def __repr__( self ):
        return self.name


def _make_debug_wrapper(funcname, func):
    def cb(*args, **kwds):
        argstr = ', '.join(list(map(repr,args)) + ['%s=%s' % item for item in kwds.items()])
        print("%s(%s)" % (funcname, argstr))
        ret = func(*args, **kwds)
        print( " <= %s" % repr(ret))
        return ret
    return cb



def use(target='desktop'):
    """ Set vispy.gl to the target OpenGL ES 2.0 implementation.
    Currently, only "desktop" is supported.
    """
    debug = vispy.config['gl_debug']
    
    # Select modules to import names from
    if target == 'desktop':
        from . import desktop as mod
    else:
        raise ValueError('Invalid target to load OpenGL API from.')
    
    # Import functions here
    NS = globals()
    funcnames = [name for name in dir(mod) if name.startswith('gl')]
    for name in funcnames:
        func = getattr(mod, name)
        if debug:
            func = _make_debug_wrapper(name, func)
        NS[name] = func
    
    # Import functions in ext
    NS = ext.__dict__
    funcnames = [name for name in dir(mod.ext) if name.startswith('gl')]
    for name in funcnames:
        func = getattr(mod.ext, name)
        if debug:
            func = _make_debug_wrapper(name, func)
        NS[name] = func


# Import ext namespace and constants
from . import ext
from ._constants import *

# Fill this namespace with functions
use()
