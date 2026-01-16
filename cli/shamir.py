"""
Command-line interface for Shamir Secret Sharing.

This CLI is intentionally minimal and deterministic.
It provides explicit split and combine operations without
implicit assumptions or hidden state.
"""

import argparse
import sys
from pathlib import Path

from shamir.core import split, combine
from shamir.format import encode_share, decode_share, ShareHeader
from shamir.errors import ShamirError


def read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def write_bytes(path: Path, data: bytes) -> None:
    path.write_bytes(data)


def cmd_split(args: argparse.Namespace) -> None:
    secret = read_bytes(Path(args.input))

    shares = split(
        secret=secret,
        threshold=args.threshold,
        share_count=args.count,
    )

    for index, payload in shares.items():
        header = ShareHeader(
            threshold=args.threshold,
            share_count=args.count,
            share_index=index,
        )
        encoded = encode_share(header, payload)
        out_path = Path(f"{args.output}.{index}")
        write_bytes(out_path, encoded)


def cmd_combine(args: argparse.Namespace) -> None:
    shares = {}

    for path_str in args.inputs:
        data = read_bytes(Path(path_str))
        header, payload = decode_share(data)
        shares[header.share_index] = payload

    secret = combine(shares)
    write_bytes(Path(args.output), secret)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Shamir Secret Sharing CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Split a secret")
    split_parser.add_argument("-i", "--input", required=True)
    split_parser.add_argument("-o", "--output", required=True)
    split_parser.add_argument("-k", "--threshold", type=int, required=True)
    split_parser.add_argument("-n", "--count", type=int, required=True)
    split_parser.set_defaults(func=cmd_split)

    combine_parser = subparsers.add_parser("combine", help="Reconstruct a secret")
    combine_parser.add_argument("-i", "--inputs", nargs="+", required=True)
    combine_parser.add_argument("-o", "--output", required=True)
    combine_parser.set_defaults(func=cmd_combine)

    args = parser.parse_args()

    try:
        args.func(args)
    except ShamirError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
