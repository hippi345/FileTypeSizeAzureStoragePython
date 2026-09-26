"""Core logic for summing blob sizes by file extension."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol


class BlobInfo(Protocol):
    """Minimal blob shape used by the calculator (Azure SDK or test doubles)."""

    name: str
    size: int


@dataclass(frozen=True)
class ContainerScanResult:
    """Blobs discovered in one container and running total for the file type."""

    container_name: str
    blobs: tuple[BlobInfo, ...]
    extension_total_bytes: int


def normalize_extension(file_type: str) -> str:
    """Ensure the extension begins with a dot for endswith matching."""
    trimmed = file_type.strip()
    if not trimmed:
        raise ValueError("file type extension cannot be empty")
    return trimmed if trimmed.startswith(".") else f".{trimmed}"


def blob_matches_extension(blob_name: str, extension: str) -> bool:
    return blob_name.endswith(extension)


def sum_matching_blob_sizes(blobs: Iterable[BlobInfo], extension: str) -> int:
    """Return total byte size of blobs whose names end with ``extension``."""
    normalized = normalize_extension(extension)
    total = 0
    for blob in blobs:
        if blob_matches_extension(blob.name, normalized):
            total += blob.size
    return total


def scan_containers(
    containers: Iterable[tuple[str, Iterable[BlobInfo]]],
    extension: str,
) -> tuple[list[ContainerScanResult], int]:
    """
    Scan containers and compute per-container blob listings plus a grand total.

    ``containers`` yields ``(container_name, blobs_iterable)`` pairs.
    """
    normalized = normalize_extension(extension)
    results: list[ContainerScanResult] = []
    grand_total = 0

    for container_name, blobs_iter in containers:
        blobs = tuple(blobs_iter)
        container_total = sum_matching_blob_sizes(blobs, normalized)
        grand_total += container_total
        results.append(
            ContainerScanResult(
                container_name=container_name,
                blobs=blobs,
                extension_total_bytes=container_total,
            )
        )

    return results, grand_total
