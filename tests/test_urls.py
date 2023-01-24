# -*- coding: utf-8 -*-

import pytest
import storefact
from storefact._urls import extract_from_query_params
import simplekv.decorator

good_urls = [
    (u'azure://MYACCOUNT:dead%2Fbeef@1buc-ket1?param1=foo&default_endpoints_protocol=http&blob_endpoint=http://host:port&create_if_missing=true', dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='dead/beef',
        container='1buc-ket1',
        create_if_missing=True,
        default_endpoints_protocol='http',
        blob_endpoint='http://host:port')),
    (u'azure://MYACCOUNT:dead%2Fbeef@1buc-ket1?param1=foo&param2=🍺&eat_more_🍎=1&create_if_missing=true', dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='dead/beef',
        container='1buc-ket1',
        create_if_missing=True)),
    (u'azure://MYACCOUNT:deadbeef@1bucket1?param1=foo&param2=🍺&eat_more_🍎=1&create_if_missing=true', dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='deadbeef',
        container='1bucket1',
        create_if_missing=True)),
    (u'azure://MYACCOUNT:deadbeef@1bucket1?param1=foo&param2=🍺&eat_more_🍎=&max_connections=5', dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='deadbeef',
        container='1bucket1',
        max_connections=5)),
    (u'azure://MYACCOUNT:deadbeef@1bucket1?param1=foo&param2=🍺&eat_more_🍎=&max_connections=5&max_block_size=4194304&&max_single_put_size=67108864', dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='deadbeef',
        container='1bucket1',
        max_connections=5,
        max_block_size=['4194304'],
        max_single_put_size=['67108864'])),
    (u'fs://this/is/a/relative/path', dict(type='fs', path='this/is/a/relative/path')),
    (u'fs:///an/absolute/path', dict(type=u'fs', path=u'/an/absolute/path')),
    (u's3://access_key:secret_key@endpoint:1234/bucketname', dict(
        type=u's3',
        host=u'endpoint:1234',
        access_key=u'access_key',
        secret_key=u'secret_key',
        bucket=u'bucketname')),
    (u'redis:///2', dict(type=u'redis', host=u'localhost', db=2)),
    (u'memory://#wrap:readonly', {'type':u'memory', 'wrap': u'readonly'}),
    (u'memory://', dict(type=u'memory')),
]

bad_urls = [
    (u'azure://MYACCOUNT:deadb/eef@1buc-ket1?param1=foo&param2=🍺&eat_more_🍎=1&create_if_missing=true',
     ValueError,
    ),
]


def test_raise_on_invalid_store():
    with pytest.raises(ValueError):
        storefact.url2dict(u'dummy://foo/bar')


@pytest.mark.parametrize('url, expected', good_urls)
def test_url2dict(url, expected):
    assert storefact.url2dict(url) == expected


@pytest.mark.parametrize('url, raises', bad_urls)
def test_bad_url2dict(url, raises):
    with pytest.raises(raises):
        storefact.url2dict(url)


def test_url2dict_with_protocol_and_point_query_params():
    url = u'azure://MYACCOUNT:dead%2Fbeef@1buc-ket1?create_if_missing=true&default_endpoints_protocol=http&blob_endpoint=http://network:888/devAcc'
    expected = dict(
        type='azure',
        account_name='MYACCOUNT',
        account_key='dead/beef',
        container='1buc-ket1',
        create_if_missing=True,
        default_endpoints_protocol="http",
        blob_endpoint="http://network:888/devAcc"
    )
    assert storefact.url2dict(url) == expected


def test_extract_query_param_when_query_params_is_null():
    query_params = None
    params = {
        'Hello': 'test'
    }
    key = "test"
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 1


def test_extract_query_param_when_query_params_is_empty():
    query_params = {}
    params = {
        'Hello': 'test'
    }
    key = "test"
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 1


def test_extract_query_param_when_params_is_null():
    query_params = {
        'create_if_missing': ['true']
    }
    params = None
    key = "test"
    extract_from_query_params(query_params, params, key)
    assert params is None


def test_extract_query_param_when_params_is_empty():
    query_params = {
        'create_if_missing': ['true']
    }
    params = {}
    key = "create_if_missing"
    extract_from_query_params(query_params, params, key, is_boolean_type=True)
    assert params is not None and len(params) == 1
    assert params[key] is True


def test_extract_query_param_when_key_is_null():
    query_params = {
        'create_if_missing': ['true']
    }
    params = {}
    key = None
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 0


def test_extract_query_param_when_key_is_empty_string():
    query_params = {
        'create_if_missing': ['true']
    }
    params = {}
    key = ''
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 0


def test_extract_query_param_when_value_is_not_boolean():
    query_params = {
        'create_if_missing': ['true']
    }
    params = {}
    key = "create_if_missing"
    extract_from_query_params(query_params, params, key, is_boolean_type=False)
    assert params is not None and len(params) == 1
    assert params[key] == 'true'


def test_extract_query_param_when_key_is_not_found_in_query_params():
    query_params = {
        'create_if_missing': ['true']
    }
    params = {}
    key = "key_not_found"
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 0


def test_extract_query_param_when_key_is_extracted():
    query_params = {
        'create_if_missing': ['true'],
        'deploy': ['now']
    }

    params = {
        'use_sas': True
    }
    key = "deploy"
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 2
    assert params['use_sas'] is True
    assert params['deploy'] == 'now'


def test_extract_query_param_when_key_already_exit():
    query_params = {
        'create_if_missing': ['true'],
        'deploy': ['now']
    }

    params = {
        'deploy': 'later'
    }

    key = "deploy"
    extract_from_query_params(query_params, params, key)
    assert params is not None and len(params) == 1
    assert params['deploy'] == 'now'


def test_roundtrip():
    assert isinstance(storefact.get_store_from_url(u'memory://#wrap:readonly'), simplekv.decorator.ReadOnlyDecorator)
