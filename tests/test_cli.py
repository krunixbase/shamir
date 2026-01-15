import subprocess
import sys
import json
import tempfile
from pathlib import Path


def run_cli(args, input_data=None):
    return subprocess.run(
        [sys.executable, "-m", "shamir"] + args,
        input=input_data,
        capture_output=True,
        check=False,
    )


def test_cli_split_and_combine_roundtrip():
    secret = b"cli-secret"
    threshold = 2
    shares = 3

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)

        secret_file = tmp / "secret.bin"
        shares_file = tmp / "shares.json"
        output_file = tmp / "recovered.bin"

        secret_file.write_bytes(secret)

        split = run_cli(
            [
                "split",
                "--threshold", str(threshold),
                "--shares", str(shares),
                "--input", str(secret_file),
                "--output", str(shares_file),
            ]
        )

        assert split.returncode == 0
        assert shares_file.exists()

        combine = run_cli(
            [
                "combine",
                "--threshold", str(threshold),
                "--input", str(shares_file),
                "--output", str(output_file),
            ]
        )

        assert combine.returncode == 0
        assert output_file.read_bytes() == secret


def test_cli_split_rejects_invalid_threshold():
    result = run_cli(
        [
            "split",
            "--threshold", "5",
            "--shares", "3",
        ],
        input_data=b"secret",
    )

    assert result.returncode != 0


def test_cli_combine_rejects_missing_input():
    result = run_cli(
        [
            "combine",
            "--threshold", "2",
        ]
    )

    assert result.returncode != 0


def test_cli_help_is_available():
    result = run_cli(["--help"])

    assert result.returncode == 0
    assert b"split" in result.stdout
    assert b"combine" in result.stdout
