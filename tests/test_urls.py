# -*- coding: utf-8 -*-

import pytest
import storefact
import simplekv.decorator

good_urls = [
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


def test_roundtrip():
    assert isinstance(storefact.get_store_from_url(u'memory://#wrap:readonly'), simplekv.decorator.ReadOnlyDecorator)
