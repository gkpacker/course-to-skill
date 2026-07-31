#!/usr/bin/env python3
"""Normalize authorized local media into transcription-ready M4A audio."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


def require_local_path(value: str) -> Path:
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        raise ValueError("input must be a local file resolved by an authorized adapter")
    return Path(value)


def build_ffmpeg_command(
    source: Path,
    output: Path,
    ffmpeg: str = "ffmpeg",
) -> list[str]:
    return [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "aac",
        "-b:a",
        "64k",
        str(output),
    ]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    args = parser.parse_args()

    source = require_local_path(args.input)
    if not source.is_file():
        raise FileNotFoundError(source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        build_ffmpeg_command(source, args.output, args.ffmpeg),
        check=True,
    )
    summary = {
        "input": source.name,
        "output": str(args.output),
        "bytes": args.output.stat().st_size,
        "checksum": "sha256:" + sha256(args.output),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
