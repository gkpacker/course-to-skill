#!/usr/bin/env python3
"""Transcribe authorized local course media with MLX Whisper."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"


def format_timestamp(seconds: float) -> str:
    total = max(0, int(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sanitize_segments(
    segments: list[dict[str, Any]], duration_seconds: float
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    previous_text = ""

    for segment in segments:
        start = float(segment.get("start", 0))
        text = normalize_text(str(segment.get("text", "")))
        reason = None
        if not text:
            reason = "empty"
        elif start >= duration_seconds - 0.05:
            reason = "starts_at_or_after_duration"
        elif text.casefold() == previous_text.casefold():
            reason = "consecutive_duplicate"

        if reason:
            rejected.append({"reason": reason, "segment": segment})
            continue

        cleaned = dict(segment)
        cleaned["text"] = text
        cleaned["end"] = min(float(segment.get("end", start)), duration_seconds)
        accepted.append(cleaned)
        previous_text = text

    return accepted, rejected


def probe_duration(audio: Path, ffprobe: str = "ffprobe") -> float:
    completed = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(audio),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    return float(payload["format"]["duration"])


def render_markdown(
    audio: Path,
    model: str,
    duration_seconds: float,
    segments: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
) -> str:
    lines = [
        "# Transcrição segmentada automática",
        "",
        "## Proveniência",
        "",
        f"- Arquivo: `{audio.name}`",
        f"- Modelo: `{model}`",
        f"- Duração: {format_timestamp(duration_seconds)}",
        f"- Segmentos rejeitados automaticamente: {len(rejected)}",
        "- Estado: requer revisão humana antes da destilação",
        "",
        "## Transcrição",
        "",
    ]
    for segment in segments:
        lines.append(f"[{format_timestamp(float(segment['start']))}] {segment['text']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def transcribe(
    audio: Path,
    model: str,
    duration_seconds: float,
    language: str | None = None,
    initial_prompt: str | None = None,
) -> dict[str, Any]:
    try:
        import mlx_whisper
    except ImportError as error:
        raise RuntimeError(
            "mlx-whisper is required; run through uv with --with mlx-whisper"
        ) from error

    options: dict[str, Any] = {
        "path_or_hf_repo": model,
        "task": "transcribe",
        "word_timestamps": True,
        "verbose": False,
        "hallucination_silence_threshold": 2.0,
    }
    if language:
        options["language"] = language
    if initial_prompt:
        options["initial_prompt"] = initial_prompt
    return mlx_whisper.transcribe(str(audio), **options)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--json-output", required=True, type=Path)
    parser.add_argument("--markdown-output", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument(
        "--language",
        default="auto",
        help="ISO language code or 'auto' for Whisper language detection",
    )
    parser.add_argument(
        "--initial-prompt",
        help="Optional course vocabulary hint; never include credentials",
    )
    parser.add_argument("--duration", type=float)
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()

    duration = args.duration or probe_duration(args.audio, args.ffprobe)
    language = None if args.language.casefold() == "auto" else args.language
    result = transcribe(
        args.audio,
        args.model,
        duration,
        language=language,
        initial_prompt=args.initial_prompt,
    )
    accepted, rejected = sanitize_segments(result.get("segments", []), duration)

    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    args.markdown_output.write_text(
        render_markdown(args.audio, args.model, duration, accepted, rejected),
        encoding="utf-8",
    )

    summary = {
        "language": result.get("language"),
        "duration_seconds": duration,
        "accepted_segments": len(accepted),
        "rejected_segments": len(rejected),
        "json_output": str(args.json_output),
        "markdown_output": str(args.markdown_output),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
