import base64
import json
import pathlib

import pytest

import storefact
from storefact._store_creation import create_store

storage = pytest.importorskip("google.cloud.storage")
from google.auth.credentials import AnonymousCredentials
from google.auth.exceptions import RefreshError


def test_create_store_gcstore(mocker):
    mock_hgcstore = mocker.patch("storefact._hstores.HGoogleCloudStore")
    mock_gcstore = mocker.patch("simplekv.net.gcstore.GoogleCloudStore")

    anon_credentials = AnonymousCredentials()
    create_store(
        "gcs",
        {
            "credentials": anon_credentials,
            "bucket_name": "test_bucket",
            "create_if_missing": True,
            "bucket_creation_location": "EUROPE-WEST1",
        },
    )
    mock_gcstore.assert_called_once_with(
        credentials=anon_credentials,
        bucket_name="test_bucket",
        create_if_missing=True,
        bucket_creation_location="EUROPE-WEST1",
    )
    mock_hgcstore.assert_not_called()


def test_create_store_hgcstore(mocker):
    mock_hgcstore = mocker.patch("storefact._hstores.HGoogleCloudStore")

    anon_credentials = AnonymousCredentials()
    create_store(
        "hgcs",
        {
            "credentials": anon_credentials,
            "bucket_name": "test_bucket",
            "create_if_missing": True,
            "bucket_creation_location": "EUROPE-WEST1",
        },
    )
    mock_hgcstore.assert_called_once_with(
        credentials=anon_credentials,
        bucket_name="test_bucket",
        create_if_missing=True,
        bucket_creation_location="EUROPE-WEST1",
    )


SHORT_URL = (
    f"gcs://{base64.urlsafe_b64encode(b'some bytes+/=asdf').decode()}"
    f"@bucket_name?create_if_missing=true&bucket_creation_location=WESTINDIES",
    {
        "type": "gcs",
        "credentials": b"some bytes+/=asdf",
        "bucket_name": "bucket_name",
        "create_if_missing": True,
        "bucket_creation_location": "WESTINDIES",
    },
)
ACTUAL_URL = (
    f"gcs://{base64.urlsafe_b64encode(pathlib.Path('tests/gcstore_cred_example.json').read_bytes()).decode()}"
    f"@default_bucket?create_if_missing=false",
    {
        "type": "gcs",
        "credentials": pathlib.Path("tests/gcstore_cred_example.json").read_bytes(),
        "bucket_name": "default_bucket",
        "create_if_missing": False,
    },
)


@pytest.mark.parametrize("url, expected", [SHORT_URL, ACTUAL_URL])
def test_url2dict(url, expected):
    assert storefact.url2dict(url) == expected


def test_json_decode():
    url, _ = ACTUAL_URL
    creds = storefact.url2dict(url)["credentials"]
    with open("tests/gcstore_cred_example.json") as file:
        assert json.loads(creds) == json.load(file)


def test_complete():
    url, expected = ACTUAL_URL
    store = storefact.get_store_from_url(url)
    assert store.bucket_name == expected["bucket_name"]
    assert store._client.project == 'central-splice-296415'
    with pytest.raises(RefreshError):
        store.get("somekey")
