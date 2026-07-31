#!/usr/bin/env python3
"""Validate the structure and audit markers of a distilled course reference."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Proveniência e estado",
    "## Essência operacional",
    "## Conteúdo sustentado",
    "## Aplicação editorial",
    "## Lacunas e revisão",
]
REQUIRED_PROVENANCE_FIELDS = [
    "**Duração:**",
    "**Estado da transcrição:**",
    "**Estado da destilação:**",
    "**Origem do título:**",
    "**Tipo:**",
    "**Cobertura:**",
]
UNCERTAINTY_PATTERN = re.compile(
    r"\[(?:inaudível|ambíguo|referência visual perdida|lacuna de passos|\?[^\]]+)\]"
)
TIMESTAMP_PATTERN = re.compile(
    r"\[(\d{1,2}):(\d{2})(?:[–-](\d{1,2}):(\d{2}))?\]"
)
ESSENCE_LABEL_PATTERN = re.compile(r"^- \[(?:decisão|ação|modelo)\]\s+")
DERIVED_LABEL_PATTERN = re.compile(r"^- \[derivado\]\s+")
NUMBER_WORD_PATTERN = re.compile(
    r"\b(?:zero|um|uma|dois|duas|três|quatro|cinco|seis|sete|oito|nove|"
    r"dez|onze|doze|treze|catorze|quatorze|quinze|dezesseis|dezessete|"
    r"dezoito|dezenove|vinte|trinta|quarenta|cinquenta|sessenta|setenta|"
    r"oitenta|noventa|cem|cento|duzentos|duzentas|trezentos|trezentas|"
    r"quatrocentos|quatrocentas|quinhentos|quinhentas|seiscentos|"
    r"seiscentas|setecentos|setecentas|oitocentos|oitocentas|novecentos|"
    r"novecentas|mil|milhão|milhões|bilhão|bilhões)\b",
    re.IGNORECASE,
)
SECRET_PATTERNS = [
    re.compile(r"api_key=", re.IGNORECASE),
    re.compile(r"access_token=", re.IGNORECASE),
    re.compile(r"authorization\s*:", re.IGNORECASE),
]
TECHNICAL_METADATA_NUMBER_PATTERN = re.compile(
    r"(?:segmentos?\s+(?:ASR\s+)?rejeitados?|versão\s+do\s+(?:motor|modelo)|"
    r"ordem\s+curricular|lesson\s+id)",
    re.IGNORECASE,
)


def section(text: str, heading: str, next_heading: str | None) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    start += len(heading)
    end = text.find(next_heading, start) if next_heading else len(text)
    return text[start : end if end >= 0 else len(text)]


def parse_duration_seconds(text: str) -> int | None:
    match = re.search(
        r"\*\*Duração(?: aproximada)?:\*\*\s*((?:\d+:)?\d{1,2}:\d{2})",
        text,
    )
    if not match:
        return None
    parts = [int(part) for part in match.group(1).split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def timestamp_seconds(text: str) -> list[int]:
    values = []
    for match in TIMESTAMP_PATTERN.finditer(text):
        values.append(int(match.group(1)) * 60 + int(match.group(2)))
        if match.group(3) is not None:
            values.append(int(match.group(3)) * 60 + int(match.group(4)))
    return values


def normalized_numbers(text: str) -> set[str]:
    scrubbed = text
    if "## Transcrição" in scrubbed:
        scrubbed = scrubbed.split("## Transcrição", 1)[1]
    elif "## Proveniência e estado" in scrubbed and "## Essência operacional" in scrubbed:
        provenance = section(
            scrubbed, "## Proveniência e estado", "## Essência operacional"
        )
        scrubbed = scrubbed.replace(provenance, "")
    scrubbed = TIMESTAMP_PATTERN.sub("", scrubbed)
    scrubbed = re.sub(
        r"\b[A-Z]{1,4}\d{1,4}-[A-Z]{1,4}\d{1,4}\b",
        "",
        scrubbed,
        flags=re.IGNORECASE,
    )
    scrubbed = re.sub(r"Seção\s+\d+", "", scrubbed)
    scrubbed = re.sub(r"Aula\s+\d+", "", scrubbed, flags=re.IGNORECASE)
    scrubbed = re.sub(
        r"(\d+(?:[.,]\d+)*)\s+vezes\b",
        r"\1x",
        scrubbed,
        flags=re.IGNORECASE,
    )
    tokens = re.findall(
        r"(?<![A-Za-z])(?:R\$\s*)?\d+(?:[.,]\d+)*(?:%|x)?(?![A-Za-z])",
        scrubbed,
    )
    return {
        token.casefold().replace("r$", "").replace(" ", "").replace(".", "")
        for token in tokens
    }


def material_lines_without_evidence(content: str) -> list[str]:
    missing: list[str] = []
    lines = content.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        if stripped.startswith("|"):
            separator_characters = set(
                stripped.replace("|", "").replace(":", "").strip()
            )
            if separator_characters <= {"-", " "}:
                continue
            next_line = lines[index + 1].strip() if index + 1 < len(lines) else ""
            if next_line.startswith("|") and "---" in next_line:
                continue
            material = True
        else:
            material = bool(
                re.match(r"^(?:-\s+|\d+\.\s+|\*\*[^*]+\*\*\s+(?:—|:))", stripped)
            )
        if material and not TIMESTAMP_PATTERN.search(stripped):
            missing.append(stripped[:100])
    return missing


def number_values_written_as_words(content: str) -> list[str]:
    heading = "### Números e limites"
    start = content.find(heading)
    if start < 0:
        return []
    block = content[start + len(heading) :]
    next_heading = block.find("\n### ")
    if next_heading >= 0:
        block = block[:next_heading]

    invalid: list[str] = []
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) < 5 or cells[2] in {"Valor dito", "---", "---:"}:
            continue
        if NUMBER_WORD_PATTERN.search(cells[2]):
            invalid.append(cells[2])
    return invalid


def technical_metadata_rows_with_timestamps(content: str) -> list[str]:
    invalid: list[str] = []
    for line in content.splitlines():
        if not line.strip().startswith("|") or not TIMESTAMP_PATTERN.search(line):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) < 5 or cells[1] in {"Item", "---"}:
            continue
        if TECHNICAL_METADATA_NUMBER_PATTERN.search(" ".join(cells[:4])):
            invalid.append(cells[1])
    return invalid


def validate(
    lesson_text: str,
    transcript_text: str | None = None,
    strict_numbers: bool = False,
) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for heading in REQUIRED_HEADINGS:
        if heading not in lesson_text:
            errors.append(f"missing heading: {heading}")

    provenance = section(lesson_text, REQUIRED_HEADINGS[0], REQUIRED_HEADINGS[1])
    for field in REQUIRED_PROVENANCE_FIELDS:
        if field not in provenance:
            errors.append(f"missing provenance field: {field}")

    if "TODO" in lesson_text:
        errors.append("lesson contains TODO placeholder")

    for pattern in SECRET_PATTERNS:
        if pattern.search(lesson_text):
            errors.append(f"lesson contains secret-like pattern: {pattern.pattern}")

    essence = section(lesson_text, REQUIRED_HEADINGS[1], REQUIRED_HEADINGS[2])
    essence_bullets = [line for line in essence.splitlines() if line.startswith("- ")]
    bullet_count = len(essence_bullets)
    if bullet_count > 3:
        errors.append(f"essence has {bullet_count} bullets; maximum is 3")
    elif bullet_count == 0 and REQUIRED_HEADINGS[1] in lesson_text:
        errors.append("essence has no bullets")
    for line in essence_bullets:
        if not ESSENCE_LABEL_PATTERN.match(line):
            errors.append(
                f"essence bullet is missing a type label: {line[:100]}"
            )
        if not TIMESTAMP_PATTERN.search(line):
            errors.append(f"essence bullet is missing temporal evidence: {line[:100]}")

    content = section(lesson_text, REQUIRED_HEADINGS[2], REQUIRED_HEADINGS[3])
    for line in material_lines_without_evidence(content):
        errors.append(f"material content is missing temporal evidence: {line}")
    for value in number_values_written_as_words(content):
        errors.append(f"number table value must use digits: {value}")
    for item in technical_metadata_rows_with_timestamps(content):
        errors.append(
            "technical metadata must not cite spoken timestamp as evidence: " + item
        )

    application = section(lesson_text, REQUIRED_HEADINGS[3], REQUIRED_HEADINGS[4])
    application_bullets = [
        line for line in application.splitlines() if line.startswith("- ")
    ]
    for line in application_bullets:
        if not DERIVED_LABEL_PATTERN.match(line):
            errors.append(f"application bullet is missing [derivado]: {line[:100]}")
        if not TIMESTAMP_PATTERN.search(line):
            errors.append(
                f"application bullet is missing temporal evidence: {line[:100]}"
            )

    if re.search(r"PORQUE\s+não informado", lesson_text, re.IGNORECASE):
        errors.append("lesson contains artificial causality: PORQUE não informado")

    duration = parse_duration_seconds(lesson_text)
    if duration is None:
        warnings.append("duration was not found in MM:SS format")
    else:
        for value in timestamp_seconds(lesson_text):
            if value > duration:
                errors.append(
                    f"timestamp {value}s exceeds declared duration {duration}s"
                )

    if transcript_text is not None:
        transcript_markers = set(UNCERTAINTY_PATTERN.findall(transcript_text))
        lesson_markers = set(UNCERTAINTY_PATTERN.findall(lesson_text))
        missing_markers = sorted(transcript_markers - lesson_markers)
        if missing_markers:
            errors.append(
                "uncertainty markers missing from lesson: " + ", ".join(missing_markers)
            )

        missing_numbers = sorted(
            normalized_numbers(transcript_text) - normalized_numbers(lesson_text)
        )
        if missing_numbers:
            message = "numbers possibly missing from lesson: " + ", ".join(
                missing_numbers
            )
            (errors if strict_numbers else warnings).append(message)

    return {"errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--transcript", type=Path)
    parser.add_argument("--strict-numbers", action="store_true")
    args = parser.parse_args()

    lesson_text = args.reference.read_text(encoding="utf-8")
    transcript_text = (
        args.transcript.read_text(encoding="utf-8") if args.transcript else None
    )
    result = validate(lesson_text, transcript_text, args.strict_numbers)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
