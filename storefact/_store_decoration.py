# -*- coding: utf-8 -*-
""""""

from __future__ import (absolute_import, division, print_function)

import reg
from simplekv.decorator import (URLEncodeKeysDecorator, ReadOnlyDecorator)


@reg.dispatch(reg.match_key('decoratorname', lambda decoratorname, store: decoratorname.split('(')[0]))
def decorate_store(store, decoratorname):
    raise ValueError('Unknown store decorator: ' + str(decoratorname))


@decorate_store.register(decoratorname='urlencode')
def _urlencode(store, decoratorname):
    return URLEncodeKeysDecorator(store)


@decorate_store.register(decoratorname='readonly')
def _readonly(store, decoratorname):
    return ReadOnlyDecorator(store)
