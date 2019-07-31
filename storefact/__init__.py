# -*- coding: utf-8 -*-
""""""
from __future__ import (absolute_import, division, print_function)

from ._compat import (PY2, reduce)
from ._store_creation import create_store
from ._store_decoration import decorate_store
from ._urls import url2dict
from ._version import version as __version__

__all__ = [
    'get_store', 'get_store_from_url', '__version__',
]


def get_store_from_url(url):
    """
    Take a URL and return a simplekv store according to the parameters in the URL.

    .. note::
       User credentials like secret keys have to be percent-encoded before they can be
       used in a URL (see *azure* and *s3* store types), since they can contain characters
       that are not valid in this part of a URL, like forward-slashes.


       You can use Python to percent-encode your secret key on the commandline like so::

           $ python -c "import urllib; print urllib.quote_plus('''dead/beef''')"
           dead%2Fbeef

    :param url: Access-URL, see below for supported forms
    :return: Parameter dictionary suitable for get_store()

    Store types and URL forms:

    * DictStore: ``memory://``
    * RedisStore: ``redis://[[password@]host[:port]][/db]``
    * FilesystemStore: ``fs://path``
    * BotoStore ``s3://access_key:secret_key@endpoint/bucket[?create_if_missing=true]``
    * AzureBlockBlockStorage: ``azure://account_name:account_key@container[?create_if_missing=true]``
    * AzureBlockBlockStorage (SAS): ``azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false``
    """
    return get_store(**url2dict(url))


def get_store(type, create_if_missing=True, **params):
    """Return a storage object according to the `type` and additional parameters.

    The *type* must be one of the types below, where each allows
    different parameters:

    * ``"azure"``: Returns a ``simplekv.azure.AzureBlockBlobStorage``. Parameters are
      ``"account_name"``, ``"account_key"``, ``"container"``, ``"use_sas"`` and ``"create_if_missing"`` (default: ``True``).
      ``"create_if_missing"`` has to be ``False`` if ``"use_sas"`` is set. When ``"use_sas"`` is set,
      ``"account_key"`` is interpreted as Shared Access Signature (SAS) token.FIRE
      ``"max_connections"``: Maximum number of network connections used by one store (default: ``2``).
      ``"socket_timeout"``: maximum timeout value in seconds (socket_timeout: ``100``).
    * ``"s3"``: Returns a plain ``simplekv.net.botostore.BotoStore``.
      Parameters must include ``"host"``, ``"bucket"``, ``"access_key"``, ``"secret_key"``.
      Optional parameters are

       - ``"force_bucket_suffix"`` (default: ``True``). If set, it is ensured that
         the bucket name ends with ``-<access_key>``
         by appending this string if necessary;
         If ``False``, the bucket name is used as-is.
       - ``"create_if_missing"`` (default: ``True`` ). If set, creates the bucket if it does not exist;
         otherwise, try to retrieve the bucket and fail with an ``IOError``.
    * ``"hs3"`` returns a variant of ``simplekv.net.botostore.BotoStore`` that allows "/" in the key name.
      The parameters are the same as for ``"s3"``
    * ``"fs"``: Returns a ``simplekv.fs.FilesystemStore``. Specify the base path as "path" parameter.
    * ``"hfs"`` returns a variant of ``simplekv.fs.FilesystemStore``  that allows "/" in the key name.
      The parameters are the same as for ``"file"``.
    * ``"memory"``: Returns a DictStore. Doesn't take any parameters
    * ``"redis"``: Returns a RedisStore. Constructs a StrictRedis using params as kwargs.
      See StrictRedis documentation for details.

    :param str type: Type of storage to open, with optional storage decorators
    :param boolean create_if_missing: Create the "root" of the storage (Azure container, parent directory, S3 bucket, etc.).
      Has no effect for stores where this makes no sense, like `redis` or `memory`.
    :param kwargs: Parameters specific to the Store-class"""

    # split off old-style wrappers, if any:
    parts = type.split('+')
    type = parts.pop(-1)
    decorators = list(reversed(parts))

    # find new-style wrappers, if any:
    wrapspec = params.pop('wrap', '')
    wrappers = list(wrapspec.split('+')) if wrapspec else []

    # can't have both:
    if wrappers:
        if decorators:
            raise ValueError('Adding store wrappers via store type as well as via wrap parameter are not allowed. Preferably use wrap.')
        decorators = wrappers

    # create_if_missing is a universal parameter, so it's part of the function signature
    # it can be safely ignored by stores where 'creating' makes no sense.
    params['create_if_missing'] = create_if_missing

    store = create_store(type, params)

    # apply wrappers/decorators:
    wrapped_store = reduce(decorate_store, decorators, store)

    return wrapped_store
