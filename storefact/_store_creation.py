# -*- coding: utf-8 -*-
""""""

from __future__ import (absolute_import, division, print_function)

import os
import os.path

from simplekv.fs import FilesystemStore
import reg


@reg.dispatch(reg.match_key('type'))
def create_store(type, params):
    raise ValueError('Unknown store type: ' + str(type))


@create_store.register(type='hazure')
@create_store.register(type='azure')
def _create_store_azure(type, params):
    from simplekv.net.azurestore import AzureBlockBlobStore
    from ._hstores import HAzureBlockBlobStore

    conn_string = params.get('connection_string', _build_azure_url(**params))
    
    if params['create_if_missing'] and params.get('use_sas', False):
        raise Exception('create_if_missing is incompatible with the use of SAS tokens.')

    if type == 'azure':
        return AzureBlockBlobStore(conn_string=conn_string, container=params['container'], public=False, create_if_missing=params['create_if_missing'])
    else:
        return HAzureBlockBlobStore(conn_string=conn_string, container=params['container'], public=False, create_if_missing=params['create_if_missing'])


@create_store.register(type='hs3')
@create_store.register(type='boto')
def _create_store_hs3(type, params):
    from ._boto import _get_s3bucket
    from ._hstores import HBotoStore
    return HBotoStore(_get_s3bucket(**params))


@create_store.register(type='s3')
def _create_store_s3(type, params):
    from simplekv.net.botostore import BotoStore
    from ._boto import _get_s3bucket
    return BotoStore(_get_s3bucket(**params))


@create_store.register(type='hfs')
@create_store.register(type='hfile')
@create_store.register(type='filesystem')
def _create_store_hfs(type, params):
    if params['create_if_missing'] and not os.path.exists(params['path']):
        os.makedirs(params['path'])
    from ._hstores import HFilesystemStore
    return HFilesystemStore(params['path'])


@create_store.register(type='fs')
@create_store.register(type='file')
def _create_store_fs(type, params):
    if params['create_if_missing'] and not os.path.exists(params['path']):
        os.makedirs(params['path'])
    return FilesystemStore(params['path'])


@create_store.register(type='memory')
def _create_store_mem(type, params):
    from simplekv.memory import DictStore
    return DictStore()


@create_store.register(type='hmemory')
def _create_store_mem(type, params):
    from ._hstores import HDictStore
    return HDictStore()


@create_store.register(type='redis')
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
