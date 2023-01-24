.. image:: https://travis-ci.org/JDASoftwareGroup/storefact.svg?branch=master
    :target: https://travis-ci.org/JDASoftwareGroup/storefact
.. image:: https://codecov.io/gh/JDASoftwareGroup/storefact/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/JDASoftwareGroup/storefact
.. image:: https://readthedocs.org/projects/storefact/badge/?version=latest
    :target: http://storefact.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

===========================
Store factory for simplekv_
===========================

A factory for simplekv_-Store-based storage classes. Takes configuration values and returns a simplekv_-Store.

This allows one to easily deploy a blob-based store in production, but test with a filesystem-based store in development.
The following simplekv_-Stores are supported in storefact:

* DictStore
* RedisStore
* FilesystemStore
* BotoStore (Amazon S3)
* AzureBlockBlobStorage


Storefact is released as open source under the 3-clause BSD license.

.. _simplekv: https://github.com/mbr/simplekv


Installation
============

::

    pip install storefact

Usage
=====
There are two possibilities to use storefact.

1) Use a dictionary with configuration data (e.g. loaded from an ini file)

.. code-block:: python

    from storefact import get_store

    params = {
        'account_name': 'test',
        'account_key': 'XXXsome_azure_account_keyXXX',
        'container': 'my-azure-container',
    }
    store = get_store('azure', **params)
    store.put(u'key', b'value')
    assert store.get(u'key') == b'value'

2) Use an URL to specify the configuration

.. code-block:: python

    from storefact import get_store_from_url, get_store

    store = get_store_from_url('azure://test:XXXsome_azure_account_keyXXX@my-azure-container')
    store.put(u'key', b'value')
    assert store.get(u'key') == b'value'

URL and store types:

* In memory: :code:`memory://` and :code:`hmemory://`.
* Redis: :code:`redis://[[password@]host[:port]][/db]` and :code:`hredis://[[password@]host[:port]][/db]`
* Filesystem: :code:`fs://` and :code:`hfs://`
* Amazon S3: :code:`s3://access_key:secret_key@endpoint/bucket[?create_if_missing=true]` and :code:`hs3://access_key:secret_key@endpoint/bucket[?create_if_missing=true]`
* Azure Blob Storage (:code:`azure://` and :code:`hazure://`):
    * with storage account key: :code:`azure://account_name:account_key@container[?create_if_missing=true][?max_connections=2]`
    * with SAS token: :code:`azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false[?max_connections=2&socket_timeout=(20,100)]`
    * with SAS and additional parameters: :code:`azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false[?max_connections=2&socket_timeout=(20,100)][?max_block_size=4*1024*1024&max_single_put_size=64*1024*1024][?default_endpoints_protocol=http&blob_endpoint=http://localhost:2121]`

Storage URLs starting with a :code:`h` indicate extended allowed characters. This allows the usage of slashes and spaces in blob names.
URL options with :code:`[]` are optional and the :code:`[]` need to be removed.

Documentation
=============

The documentation can be found on readthedocs_.

.. _readthedocs: https://storefact.readthedocs.io/

Development
===========

To run the all tests run::

    tox

