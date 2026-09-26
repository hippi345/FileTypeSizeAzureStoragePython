"""Tests for Azure client wiring (mocked SDK)."""

from unittest.mock import MagicMock, patch

from filetype_size.azure_client import create_blob_service_client, iter_containers_with_blobs


def test_create_blob_service_client_url():
    with patch("filetype_size.azure_client.BlobServiceClient") as mock_cls:
        create_blob_service_client("myacct", "secret")
        mock_cls.assert_called_once_with(
            account_url="https://myacct.blob.core.windows.net",
            credential="secret",
        )


def test_iter_containers_with_blobs():
    client = MagicMock()
    container = MagicMock()
    container.name = "logs"
    client.list_containers.return_value = [container]

    container_client = MagicMock()
    blob = MagicMock()
    blob.name = "app.log"
    blob.size = 99
    container_client.list_blobs.return_value = [blob]
    client.get_container_client.return_value = container_client

    pairs = list(iter_containers_with_blobs(client))
    assert pairs == [("logs", [pairs[0][1][0]])]
    assert pairs[0][1][0].name == "app.log"
    assert pairs[0][1][0].size == 99
