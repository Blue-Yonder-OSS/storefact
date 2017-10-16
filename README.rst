.. image:: https://travis-ci.org/blue-yonder/storefact.svg?branch=master
    :target: https://travis-ci.org/blue-yonder/storefact
.. image:: https://coveralls.io/repos/github/blue-yonder/storefact/badge.svg?branch=master
    :target: https://coveralls.io/github/blue-yonder/storefact?branch=master
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

Documentation
=============

The documentation can be found on readthedocs_.

.. _readthedocs: https://storefact.readthedocs.io/

Development
===========

To run the all tests run::

    tox

