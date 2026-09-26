# FileTypeSizeAzureStoragePython

[![CI](https://github.com/hippi345/FileTypeSizeAzureStoragePython/actions/workflows/ci.yml/badge.svg)](https://github.com/hippi345/FileTypeSizeAzureStoragePython/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Calculate the **total byte size** of blobs matching a file extension across all containers in an Azure Storage account—for example, sum every `.vhd` or `.png` in the account.

The tool uses the current [Azure Storage Blob SDK for Python](https://learn.microsoft.com/en-us/python/api/azure-storage-blob/) (`azure-storage-blob` v12+). Credentials are read from the environment or interactive prompts; they are never stored in the repository.

## Features

- Lists every container and blob (name and size) in the storage account
- Totals sizes for blobs whose names end with your chosen extension (e.g. `.vhd`)
- Supports non-interactive runs via environment variables
- Offline unit tests with mocked Azure clients

## Requirements

- Python **3.12+**
- An Azure Storage account with account name and key (or use a connection string pattern via env vars above)

## Setup

```bash
git clone https://github.com/hippi345/FileTypeSizeAzureStoragePython.git
cd FileTypeSizeAzureStoragePython
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` and fill in values locally (`.env` is gitignored).

## Configuration

| Variable | Description |
| -------- | ----------- |
| `AZURE_STORAGE_ACCOUNT_NAME` | Storage account name |
| `AZURE_STORAGE_ACCOUNT_KEY` | Storage account access key |
| `FILE_TYPE` | Extension to match (e.g. `.vhd` or `vhd`) |

If any variable is missing, the program prompts for it on stdin.

## Usage

**With environment variables:**

```bash
export AZURE_STORAGE_ACCOUNT_NAME=myaccount
export AZURE_STORAGE_ACCOUNT_KEY='...'
export FILE_TYPE=.vhd
python main.py
```

**Console script (after install):**

```bash
filetype-size-azure
```

**Interactive (no env vars):**

```bash
python main.py
```

Example output:

```
Welcome to the file size calculator for Azure Storage on Python
Printing out containers:
     my-container:
Blob name: backups/disk.vhd
Blob size: 1073741824
Total size of .vhd files: 1073741824
```

## Running tests

Tests run fully offline with mocked Azure APIs:

```bash
ruff check .
ruff format --check .
pytest --cov=filetype_size
```

## Project structure

```
├── filetype_size/
│   ├── azure_client.py   # BlobServiceClient helpers
│   ├── calculator.py     # Extension matching and totals
│   └── cli.py            # Prompts / env / output
├── main.py               # Entry point
├── tests/
├── pyproject.toml        # Package metadata and tool config
├── requirements.txt      # Runtime pins (source)
└── requirements.lock     # Locked versions for CI/reproducible installs
```

## License

MIT License — see [LICENSE](LICENSE) (Copyright © 2026 Joel Shearon).
