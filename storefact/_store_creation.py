# -*- coding: utf-8 -*-
""""""

from __future__ import (absolute_import, division, print_function)

import os
import os.path

from simplekv.fs import FilesystemStore


def create_store(type, params):
    if type in ('azure', 'hazure'):
        return _create_store_azure(type, params)
    if type in ('hs3', 'boto'):
        return _create_store_hs3(type, params)
    if type in ('s3'):
        return _create_store_s3(type, params)
    if type in ('hfs', 'hfile', 'filesystem'):
        return _create_store_hfs(type, params)
    if type in ('fs', 'file'):
        return _create_store_fs(type, params)
    if type in ('memory'):
        return _create_store_mem(type, params)
    if type in ('hmemory'):
        return _create_store_hmem(type, params)
    if type in ('redis'):
        return _create_store_redis(type, params)
    raise ValueError('Unknown store type: ' + str(type))


def _create_store_azure(type, params):
    from simplekv.net.azurestore import AzureBlockBlobStore
    from ._hstores import HAzureBlockBlobStore

    conn_string = params.get('connection_string', _build_azure_url(**params))

    if params['create_if_missing'] and params.get('use_sas', False):
        raise Exception('create_if_missing is incompatible with the use of SAS tokens.')

    if type == 'azure':
        return AzureBlockBlobStore(
            conn_string=conn_string,
            container=params['container'],
            public=False,
            create_if_missing=params['create_if_missing'],
            checksum=params.get('checksum', True),
            max_connections=params.get('max_connections', 2),
            socket_timeout=params.get('socket_timeout', (20, 100)),
        )
    else:
        return HAzureBlockBlobStore(
            conn_string=conn_string,
            container=params['container'],
            public=False,
            create_if_missing=params['create_if_missing'],
            checksum=params.get('checksum', True),
            max_connections=params.get('max_connections', 2),
            socket_timeout=params.get('socket_timeout', (20, 100)),
        )


def _create_store_hs3(type, params):
    from ._boto import _get_s3bucket
    from ._hstores import HBotoStore
    return HBotoStore(_get_s3bucket(**params))


def _create_store_s3(type, params):
    from simplekv.net.botostore import BotoStore
    from ._boto import _get_s3bucket
    return BotoStore(_get_s3bucket(**params))


def _create_store_hfs(type, params):
    if params['create_if_missing'] and not os.path.exists(params['path']):
        os.makedirs(params['path'])
    from ._hstores import HFilesystemStore
    return HFilesystemStore(params['path'])


def _create_store_fs(type, params):
    if params['create_if_missing'] and not os.path.exists(params['path']):
        os.makedirs(params['path'])
    return FilesystemStore(params['path'])


def _create_store_mem(type, params):
    from simplekv.memory import DictStore
    return DictStore()


def _create_store_hmem(type, params):
    from ._hstores import HDictStore
    return HDictStore()


def _create_store_redis(type, params):
    from simplekv.memory.redisstore import RedisStore
    from redis import StrictRedis
    r = StrictRedis(**params)
    return RedisStore(r)


def _build_azure_url(
    account_name=None, account_key=None, default_endpoints_protocol=None, blob_endpoint=None,
        use_sas=False, **kwargs):
    protocol = default_endpoints_protocol or 'https'
    if use_sas:
        return ('DefaultEndpointsProtocol={protocol};AccountName={account_name};'
                'SharedAccessSignature={shared_access_signature}'.format(
                    protocol=protocol, account_name=account_name, shared_access_signature=account_key))
    else:
        return 'DefaultEndpointsProtocol={protocol};AccountName={account_name};AccountKey={account_key}'.format(
            protocol=protocol, account_name=account_name, account_key=account_key)
