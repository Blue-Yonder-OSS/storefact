# -*- coding: utf-8 -*-

import reg
from uritools import urisplit


TRUEVALUES = (u'true',)


def url2dict(url, raise_on_extra_params=False):
    """

    :param url: Access-URL, see below for supported forms
    :return: Parameter dictionary suitable for get_store()

    memory://
    redis://[[password@]host[:port]][/db]
    fs://path
    s3://access_key:secret_key@endpoint/bucket[?create_if_missing=true]
    azure://account_name:account_key@container[?create_if_missing=true]
    azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false
    """
    u = urisplit(url)
    parsed = dict(
        scheme=u.getscheme(),
        host=u.gethost(),
        port=u.getport(),
        path=u.getpath(),
        query=u.getquerydict(),
        userinfo=u.getuserinfo(),
    )
    fragment = u.getfragment()

    params = {'type': parsed['scheme']}

    # handling special instructions embedded in the 'fragment' part of the URL,
    # currently only wrappers/store decorators
    fragments = fragment.split('#') if fragment else []
    wrap_spec = list(filter(lambda s: s.startswith('wrap:'), fragments))
    if wrap_spec:
        wrappers = wrap_spec[-1].partition('wrap:')[2]  # remove the 'wrap:' part
        params['wrap'] = wrappers

    if u'create_if_missing' in parsed['query']:
        create_if_missing = parsed['query'].pop(u'create_if_missing')[-1]  # use last appearance of key
        params['create_if_missing'] = create_if_missing in TRUEVALUES

    # get store-specific parameters:
    store_params = extract_params(**parsed)
    params.update(store_params)
    return params


@reg.dispatch(reg.match_key('scheme', lambda scheme, host, port, path, query, userinfo: scheme))
def extract_params(scheme, host, port, path, query, userinfo):
    raise ValueError('Unknown storage type "{}"'.format(scheme))


@extract_params.register(scheme='hmemory')
@extract_params.register(scheme='memory')
def extract_params_memory(scheme, host, port, path, query, userinfo):
    return {}


@extract_params.register(scheme='hredis')
@extract_params.register(scheme='redis')
def extract_params_redis(scheme, host, port, path, query, userinfo):
    path = path[1:] if path.startswith(u'/') else path
    params = {'host': host or u'localhost'}
    if port:
        params['port'] = port
    if userinfo:
        params['password'] = userinfo
    if path:
        params['db'] = int(path)
    return params


@extract_params.register(scheme='fs')
@extract_params.register(scheme='hfs')
def extract_params_fs(scheme, host, port, path, query, userinfo):
    return {'type': scheme, 'path': host + path}


@extract_params.register(scheme='s3')
@extract_params.register(scheme='hs3')
def extract_params_s3(scheme, host, port, path, query, userinfo):
    access_key, secret_key = _parse_userinfo(userinfo)
    params = {
        'host': u'{}:{}'.format(host, port) if port else host,
        'access_key': access_key,
        'secret_key': secret_key,
        'bucket': path[1:],
    }
    return params


@extract_params.register(scheme='hazure')
@extract_params.register(scheme='azure')
def extract_params_azure(scheme, host, port, path, query, userinfo):
    account_name, account_key = _parse_userinfo(userinfo)
    params = {
        'account_name': account_name,
        'account_key': account_key,
        'container': host,
    }
    if u'use_sas' in query:
        params['use_sas'] = True
    return params


def _parse_userinfo(userinfo):
    """Try to split the URL's userinfo (the part between :// and @) into fields
    separated by :. If anything looks wrong, remind user to percent-encode values."""
    if hasattr(userinfo, 'split'):
        parts = userinfo.split(u':', 1)

        if len(parts) == 2:
            return parts

    raise ValueError('Could not parse user/key in store-URL. Note that values have to be percent-encoded, eg. with urllib.quote_plus().')

