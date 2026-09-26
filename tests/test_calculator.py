"""Unit tests for extension matching and size aggregation."""

from dataclasses import dataclass

import pytest

from filetype_size.calculator import (
    blob_matches_extension,
    normalize_extension,
    scan_containers,
    sum_matching_blob_sizes,
)


@dataclass
class FakeBlob:
    name: str
    size: int


def test_normalize_extension_adds_leading_dot():
    assert normalize_extension("vhd") == ".vhd"
    assert normalize_extension(".png") == ".png"


def test_normalize_extension_rejects_empty():
    with pytest.raises(ValueError):
        normalize_extension("  ")


def test_sum_matching_blob_sizes():
    blobs = [
        FakeBlob("data/file.vhd", 100),
        FakeBlob("data/file.png", 50),
        FakeBlob("other.vhd", 25),
    ]
    assert sum_matching_blob_sizes(blobs, ".vhd") == 125


def test_blob_matches_extension():
    assert blob_matches_extension("path/to/blob.VHD", ".VHD") is True
    assert blob_matches_extension("path/to/blob.vhd", ".vhd") is True
    assert blob_matches_extension("path/to/blob.vhd", ".VHD") is False


def test_scan_containers_grand_total():
    containers = [
        ("c1", [FakeBlob("a.vhd", 10), FakeBlob("b.txt", 5)]),
        ("c2", [FakeBlob("c.vhd", 20)]),
    ]
    results, total = scan_containers(containers, "vhd")
    assert len(results) == 2
    assert total == 30
    assert results[0].extension_total_bytes == 10
    assert results[1].extension_total_bytes == 20
