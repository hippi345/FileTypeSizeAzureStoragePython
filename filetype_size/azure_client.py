"""Azure Blob Storage client helpers."""

from __future__ import annotations

from collections.abc import Iterator

from azure.storage.blob import BlobServiceClient

from filetype_size.calculator import BlobInfo


class ListedBlob:
    """Adapter exposing name and size for calculator protocols."""

    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


def create_blob_service_client(account_name: str, account_key: str) -> BlobServiceClient:
    account_url = f"https://{account_name}.blob.core.windows.net"
    return BlobServiceClient(account_url=account_url, credential=account_key)


def iter_containers_with_blobs(
    client: BlobServiceClient,
) -> Iterator[tuple[str, list[BlobInfo]]]:
    """List every container and its blobs (name + size)."""
    for container in client.list_containers():
        name = container.name
        container_client = client.get_container_client(name)
        blobs: list[BlobInfo] = [
            ListedBlob(blob.name, blob.size) for blob in container_client.list_blobs()
        ]
        yield name, blobs
