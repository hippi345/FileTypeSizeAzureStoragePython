"""Command-line interface (interactive prompts or environment variables)."""

from __future__ import annotations

import os
import sys
from typing import TextIO

from azure.core.exceptions import AzureError

from filetype_size.azure_client import create_blob_service_client, iter_containers_with_blobs
from filetype_size.calculator import normalize_extension, scan_containers


def _read_config(
    stdin: TextIO,
    stdout: TextIO,
) -> tuple[str, str, str]:
    account = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME", "").strip()
    key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY", "").strip()
    file_type = os.environ.get("FILE_TYPE", "").strip()

    if not account:
        stdout.write("What is your storage account name?\n")
        stdout.flush()
        account = stdin.readline().strip()
    if not key:
        stdout.write("What is your storage account key?\n")
        stdout.flush()
        key = stdin.readline().strip()
    if not file_type:
        stdout.write(
            "What kind of file path are you curious about getting the size on? "
            "(ex. .vhd, .png, .gif, etc.)\n"
        )
        stdout.flush()
        file_type = stdin.readline().strip()

    if not account or not key or not file_type:
        raise ValueError("Storage account name, key, and file type are all required.")

    return account, key, file_type


def run(stdout: TextIO | None = None, stdin: TextIO | None = None) -> int:
    """Run the size calculator; returns process exit code."""
    out = stdout or sys.stdout
    inp = stdin or sys.stdin

    out.write("Welcome to the file size calculator for Azure Storage on Python\n")

    try:
        account_name, account_key, file_type = _read_config(inp, out)
        extension = normalize_extension(file_type)
    except ValueError as exc:
        out.write(f"Error: {exc}\n")
        return 1

    try:
        client = create_blob_service_client(account_name, account_key)
        container_data = list(iter_containers_with_blobs(client))
        results, grand_total = scan_containers(container_data, extension)
    except AzureError as exc:
        out.write(f"Azure Storage error: {exc}\n")
        return 1

    out.write("Printing out containers:\n")
    for result in results:
        out.write(f"     {result.container_name}:\n")
        for blob in result.blobs:
            out.write(f"Blob name: {blob.name}\n")
            out.write(f"Blob size: {blob.size}\n")

    out.write(f"Total size of {extension} files: {grand_total}\n")
    return 0


def main() -> None:
    raise SystemExit(run())
