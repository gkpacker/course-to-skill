#!/usr/bin/env python3
"""Create a safe local repository scaffold for a course knowledge skill."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_value.casefold()).strip("-")
    if not slug:
        raise ValueError("title must contain at least one letter or digit")
    return slug[:63].rstrip("-")


def render_tree(
    template_root: Path,
    output: Path,
    values: dict[str, str],
) -> list[str]:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"output directory is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    for source in sorted(template_root.rglob("*")):
        relative = source.relative_to(template_root)
        rendered_parts = []
        for part in relative.parts:
            rendered = part
            for token, value in values.items():
                rendered = rendered.replace(token, value)
            rendered_parts.append(rendered)
        destination = output.joinpath(*rendered_parts)
        if destination.name.endswith(".tmpl"):
            destination = destination.with_name(destination.name.removesuffix(".tmpl"))

        if source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        text = source.read_text(encoding="utf-8")
        for token, value in values.items():
            text = text.replace(token, value)
        unresolved = sorted(set(re.findall(r"__[A-Z0-9_]+__", text)))
        if unresolved:
            raise ValueError(
                f"unresolved template tokens in {source}: {', '.join(unresolved)}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")
        created.append(str(destination.relative_to(output)))

    for relative in [
        "corpus/transcripts",
        "state/audio",
        f"skills/{values['__COURSE_SLUG__']}/references/generated",
    ]:
        (output / relative).mkdir(parents=True, exist_ok=True)
    return created


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--slug")
    parser.add_argument("--visibility", choices=["private", "public"], default="private")
    parser.add_argument("--default-language", default="auto")
    parser.add_argument("--github-owner")
    parser.add_argument("--repository-name")
    args = parser.parse_args()

    slug = slugify(args.slug or args.title)
    is_public = args.visibility == "public"
    visibility_ignores = ""
    if is_public:
        visibility_ignores = (
            "# Course content excluded until redistribution rights are confirmed\n"
            "corpus/transcripts/\n"
            f"skills/{slug}/references/generated/\n"
        )

    values = {
        "__COURSE_TITLE__": args.title,
        "__COURSE_SLUG__": slug,
        "__VISIBILITY__": args.visibility,
        "__DEFAULT_LANGUAGE__": args.default_language,
        "__VERSION_TRANSCRIPTS__": "false" if is_public else "true",
        "__VERSION_REFERENCES__": "false" if is_public else "true",
        "__VISIBILITY_IGNORES__": visibility_ignores.rstrip(),
    }
    template_root = Path(__file__).resolve().parents[1] / "assets" / "project-template"
    created = render_tree(template_root, args.output.resolve(), values)

    repository_name = args.repository_name or f"{slug}-skills"
    owner_prefix = f"{args.github_owner}/" if args.github_owner else "OWNER/"
    visibility_flag = "--public" if is_public else "--private"
    summary = {
        "output": str(args.output.resolve()),
        "course_slug": slug,
        "visibility": args.visibility,
        "created_files": created,
        "next_steps": [
            f"Review {args.output.resolve()}",
            "Run the generated tests and secret scan",
            f"cd {args.output.resolve()}",
            "git init -b main && git add . && git commit -m 'Initialize course skill'",
            f"gh repo create {owner_prefix}{repository_name} {visibility_flag} --source . --remote origin --push",
        ],
        "requires_public_confirmation": is_public,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
