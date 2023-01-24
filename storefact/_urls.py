# -*- coding: utf-8 -*-

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
    azure://account_name:account_key@container[?create_if_missing=true][?max_connections=2]
    azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false[?max_connections=2&socket_timeout=(20,100)]
    azure://account_name:shared_access_signature@container?use_sas&create_if_missing=false[?max_connections=2&socket_timeout=(20,100)][?max_block_size=4*1024*1024&max_single_put_size=64*1024*1024]
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

    extract_from_query_params(parsed['query'], params, "create_if_missing", is_boolean_type=True)
    extract_from_query_params(parsed['query'], params, "blob_endpoint")
    extract_from_query_params(parsed['query'], params, "default_endpoints_protocol")

    # get store-specific parameters:
    store_params = extract_params(**parsed)
    params.update(store_params)
    return params


def extract_from_query_params(query_params, params, key, is_boolean_type=False):
    """

    Args:
        query_params: dictionary to extract from
        params: dictionary to extract to
        key: key to look for in query_params
        is_boolean_type: if expected value is in Boolean True, False then pass the value as True.
        Default is False.

    Returns:
        None
    note: Updates the params dictionary as objects are pass by reference

    """
    if query_params and params is not None and key in query_params:
        value = query_params.pop(key)[-1]
        if is_boolean_type:
            value = value in TRUEVALUES
        params[key] = value


def extract_params(scheme, host, port, path, query, userinfo):
    if scheme in ('memory', 'hmemory'):
        return {}
    if scheme in ('redis', 'hredis'):
        path = path[1:] if path.startswith(u'/') else path
        params = {'host': host or u'localhost'}
        if port:
            params['port'] = port
        if userinfo:
            params['password'] = userinfo
        if path:
            params['db'] = int(path)
        return params
    if scheme in ('fs', 'hfs'):
        return {'type': scheme, 'path': host + path}
    if scheme in ('s3', 'hs3'):
        access_key, secret_key = _parse_userinfo(userinfo)
        params = {
            'host': u'{}:{}'.format(host, port) if port else host,
            'access_key': access_key,
            'secret_key': secret_key,
            'bucket': path[1:],
        }
        return params
    if scheme in ('azure', 'hazure'):
        account_name, account_key = _parse_userinfo(userinfo)
        params = {
            'account_name': account_name,
            'account_key': account_key,
            'container': host,
        }
        if u'use_sas' in query:
            params['use_sas'] = True
        if u'max_connections' in query:
            params['max_connections'] = int(query.pop(u'max_connections')[-1])
        if u'socket_timeout' in query:
            params['socket_timeout'] = query.pop(u'socket_timeout')
        if u'max_block_size' in query:
            params['max_block_size'] = query.pop(u'max_block_size')
        if u'max_single_put_size' in query:
            params['max_single_put_size'] = query.pop(u'max_single_put_size')
        return params

    raise ValueError('Unknown storage type "{}"'.format(scheme))


def _parse_userinfo(userinfo):
    """Try to split the URL's userinfo (the part between :// and @) into fields
    separated by :. If anything looks wrong, remind user to percent-encode values."""
    if hasattr(userinfo, 'split'):
        parts = userinfo.split(u':', 1)

        if len(parts) == 2:
            return parts

    raise ValueError('Could not parse user/key in store-URL. Note that values have to be percent-encoded, eg. with urllib.quote_plus().')

