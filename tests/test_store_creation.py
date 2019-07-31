from storefact._store_creation import create_store
import pytest


def test_create_store_azure(mocker):
    # Mock HAzureBlockBlobStore also here, becase otherwise it will try to inherit from
    # the mock object `mock_azure` created below, which will fail.
    mock_hazure = mocker.patch("storefact._hstores.HAzureBlockBlobStore")
    mock_azure = mocker.patch("simplekv.net.azurestore.AzureBlockBlobStore")
    create_store(
        "azure",
        {
            "account_name": "ACCOUNT",
            "account_key": "KEY",
            "container": "cont_name",
            "create_if_missing": True,
        },
    )
    mock_azure.assert_called_once_with(
        checksum=True,
        conn_string="DefaultEndpointsProtocol=https;AccountName=ACCOUNT;AccountKey=KEY",
        container="cont_name",
        create_if_missing=True,
        max_connections=2,
        public=False,
        socket_timeout=(20, 100),
    )
    mock_hazure.assert_not_called()


def test_create_store_hazure(mocker):
    mock_hazure = mocker.patch("storefact._hstores.HAzureBlockBlobStore")
    create_store(
        "hazure",
        {
            "account_name": "ACCOUNT",
            "account_key": "KEY",
            "container": "cont_name",
            "create_if_missing": True,
        },
    )
    mock_hazure.assert_called_once_with(
        checksum=True,
        conn_string="DefaultEndpointsProtocol=https;AccountName=ACCOUNT;AccountKey=KEY",
        container="cont_name",
        create_if_missing=True,
        max_connections=2,
        public=False,
        socket_timeout=(20, 100),
    )


def test_create_store_azure_inconsistent_params():
    with pytest.raises(
            Exception, match="create_if_missing is incompatible with the use of SAS tokens"
    ):
        create_store(
            "hazure",
            {
                "account_name": "ACCOUNT",
                "account_key": "KEY",
                "container": "cont_name",
                "create_if_missing": True,
                "use_sas": True,
            },
        )


def test_create_store_hs3(mocker):
    mock_hs3 = mocker.patch("storefact._boto._get_s3bucket")
    mock_hbotostores = mocker.patch("storefact._hstores.HBotoStore")
    create_store(
        "hs3",
        {
            'host': u'endpoint:1234',
            'access_key': u'access_key',
            'secret_key': u'secret_key',
            'bucket': u'bucketname',
        },
    )
    mock_hs3.assert_called_once_with(
        host=u'endpoint:1234',
        access_key=u'access_key',
        secret_key=u'secret_key',
        bucket=u'bucketname',
    )


def test_create_store_s3(mocker):
    mock_s3 = mocker.patch("storefact._boto._get_s3bucket")
    mock_hbotostores = mocker.patch("storefact._hstores.HBotoStore")
    create_store(
        "s3",
        {
            'host': u'endpoint:1234',
            'access_key': u'access_key',
            'secret_key': u'secret_key',
            'bucket': u'bucketname',
        },
    )
    mock_s3.assert_called_once_with(
        host=u'endpoint:1234',
        access_key=u'access_key',
        secret_key=u'secret_key',
        bucket=u'bucketname',
    )


def test_create_store_hfs(mocker):
    mock_hfs = mocker.patch("storefact._hstores.HFilesystemStore")
    create_store(
        "hfs",
        {
            'type': 'hfs',
            'path': 'this/is/a/relative/path',
            'create_if_missing': True
        },
    )
    mock_hfs.assert_called_once_with('this/is/a/relative/path')


@pytest.mark.skip(reason="some issue here")
def test_create_store_fs(mocker):
    mock_fs = mocker.patch("simplekv.fs.FilesystemStore")
    create_store(
        "fs",
        {
            'type': 'fs',
            'path': 'this/is/a/relative/fspath',
            'create_if_missing': True
        }
    )
    mock_fs.assert_called_once_with('this/is/a/relative/fspath')


def test_create_store_mem(mocker):
    mock_mem = mocker.patch("simplekv.memory.DictStore")
    create_store(
        "memory",
        {'type': u'memory', 'wrap': u'readonly'},
    )
    mock_mem.assert_called_once_with()


def test_create_store_hmem(mocker):
    mock_hmem = mocker.patch("storefact._hstores.HDictStore")
    create_store(
        "hmemory",
        {'type': u'memory', 'wrap': u'readonly'},
    )
    mock_hmem.assert_called_once_with()


@pytest.mark.skip(reason="some issue here")
def test_create_store_redis(mocker):
    mock_redis = mocker.patch("simplekv.memory.redisstore.RedisStore")
    mock_Strictredis = mocker.patch("redis.StrictRedis")
    create_store(
        "redis",
        {'type': u'redis', 'host': u'localhost', 'db': 2},
    )
    mock_Strictredis.assert_called_once_with()


def test_create_store_valueerror():
    with pytest.raises(
            Exception, match="Unknown store type: ABC"
    ):
        create_store(
            "ABC",
            {
                "account_name": "ACCOUNT",
                "account_key": "KEY",
                "container": "cont_name",
                "create_if_missing": True,
                "use_sas": True,
            },
        )
