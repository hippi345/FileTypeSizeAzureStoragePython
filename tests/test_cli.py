"""CLI tests with mocked Azure client."""

from io import StringIO
from unittest.mock import MagicMock, patch

from filetype_size.azure_client import ListedBlob
from filetype_size.cli import run


@patch("filetype_size.cli.create_blob_service_client")
@patch("filetype_size.cli.iter_containers_with_blobs")
def test_run_with_env_vars(mock_iter, mock_create):
    mock_create.return_value = MagicMock()
    mock_iter.return_value = [
        ("images", [ListedBlob("photo.png", 100), ListedBlob("disk.vhd", 500)]),
    ]

    stdin = StringIO("")
    stdout = StringIO()
    env = {
        "AZURE_STORAGE_ACCOUNT_NAME": "myaccount",
        "AZURE_STORAGE_ACCOUNT_KEY": "fake-key",
        "FILE_TYPE": ".vhd",
    }

    with patch.dict("os.environ", env, clear=False):
        code = run(stdout=stdout, stdin=stdin)

    assert code == 0
    output = stdout.getvalue()
    assert "images" in output
    assert "Total size of .vhd files: 500" in output
    mock_create.assert_called_once_with("myaccount", "fake-key")


@patch("filetype_size.cli.create_blob_service_client")
def test_run_interactive_prompts(mock_create):
    mock_create.return_value = MagicMock()

    stdin = StringIO("acct\nkey\n.png\n")
    stdout = StringIO()

    with patch.dict("os.environ", {}, clear=True):
        with patch(
            "filetype_size.cli.iter_containers_with_blobs",
            return_value=[("c", [ListedBlob("x.png", 42)])],
        ):
            code = run(stdout=stdout, stdin=stdin)

    assert code == 0
    assert "Total size of .png files: 42" in stdout.getvalue()
