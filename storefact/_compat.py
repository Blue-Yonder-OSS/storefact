# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys

PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr
    binary_type = str
    from itertools import imap
    reduce = reduce
    xrange = xrange
    from ConfigParser import ConfigParser
    from cStringIO import StringIO as BytesIO
    import cPickle as pickle
    import copy_reg as copyreg
else:
    text_type = str
    string_types = (str,)
    unichr = chr
    binary_type = bytes
    imap = map
    from functools import reduce
    xrange = range
    from configparser import ConfigParser
    from io import BytesIO
    import pickle
    import copyreg
