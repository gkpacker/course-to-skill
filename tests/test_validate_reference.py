from __future__ import annotations

import unittest

from _loader import load_script

validate_reference = load_script("validate_reference")


def valid_lesson() -> str:
    return """# Aula de teste

## Proveniência e estado

- **Duração:** 01:00
- **Estado da transcrição:** revisada
- **Estado da destilação:** validada
- **Origem do título:** portal
- **Tipo:** conceitual
- **Cobertura:** completa

## Essência operacional

- [modelo] Distinguir dois conceitos. [00:01–00:10]

## Conteúdo sustentado

**Conceito** — definição sustentada. [00:01–00:10]

## Aplicação editorial

- [derivado] Usar para distinguir os conceitos. [00:01–00:10]

## Lacunas e revisão

Nenhuma lacuna material.
"""


class ValidateReferenceTest(unittest.TestCase):
    def test_valid_reference_passes_structural_validation(self) -> None:
        result = validate_reference.validate(valid_lesson())
        self.assertEqual(result, {"errors": [], "warnings": []})

    def test_detects_missing_heading_and_too_many_essence_bullets(self) -> None:
        lesson = valid_lesson().replace("## Lacunas e revisão", "## Revisão")
        lesson = lesson.replace(
            "- [modelo] Distinguir dois conceitos. [00:01–00:10]",
            "\n".join(
                f"- [ação] Executar ação {index}. [00:01]" for index in range(4)
            ),
        )
        result = validate_reference.validate(lesson)
        self.assertTrue(any("missing heading" in error for error in result["errors"]))
        self.assertTrue(
            any("essence has 4 bullets" in error for error in result["errors"])
        )

    def test_requires_evidence_and_labels_for_synthesis(self) -> None:
        lesson = valid_lesson().replace(
            "- [modelo] Distinguir dois conceitos. [00:01–00:10]",
            "- Distinguir dois conceitos.",
        ).replace(
            "- [derivado] Usar para distinguir os conceitos. [00:01–00:10]",
            "- Usar para distinguir os conceitos.",
        )
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any(
                "essence bullet is missing a type label" in error
                for error in result["errors"]
            )
        )
        self.assertTrue(
            any(
                "application bullet is missing [derivado]" in error
                for error in result["errors"]
            )
        )
        self.assertTrue(
            any("missing temporal evidence" in error for error in result["errors"])
        )

    def test_detects_material_content_without_evidence(self) -> None:
        lesson = valid_lesson().replace(
            "**Conceito** — definição sustentada. [00:01–00:10]",
            "**Conceito** — definição sem evidência.",
        )
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any(
                "material content is missing temporal evidence" in error
                for error in result["errors"]
            )
        )

    def test_detects_artificial_causality(self) -> None:
        lesson = valid_lesson() + "\nSE algo ENTÃO faça algo PORQUE não informado.\n"
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any("artificial causality" in error for error in result["errors"])
        )

    def test_detects_timestamp_after_duration(self) -> None:
        lesson = valid_lesson().replace("[00:01–00:10]", "[00:01–01:01]", 1)
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any("exceeds declared duration" in error for error in result["errors"])
        )

    def test_detects_removed_uncertainty_marker(self) -> None:
        transcript = "[00:01] A ferramenta [?Nome] custou R$ 20."
        result = validate_reference.validate(valid_lesson(), transcript)
        self.assertTrue(
            any("uncertainty markers missing" in error for error in result["errors"])
        )

    def test_strict_numbers_promotes_warning_to_error(self) -> None:
        transcript = "[00:01] O valor é 37%."
        result = validate_reference.validate(
            valid_lesson(), transcript, strict_numbers=True
        )
        self.assertTrue(
            any("numbers possibly missing" in error for error in result["errors"])
        )

    def test_normalizes_spoken_multipliers(self) -> None:
        lesson = valid_lesson().replace(
            "**Conceito** — definição sustentada. [00:01–00:10]",
            "**Comparação** — o item custa 40x mais. [00:01–00:10]",
        )
        transcript = "[00:01] O item custa 40 vezes mais."
        result = validate_reference.validate(lesson, transcript, strict_numbers=True)
        self.assertFalse(
            any("numbers possibly missing" in error for error in result["errors"])
        )

    def test_number_comparison_ignores_asr_metadata_and_alphanumeric_terms(self) -> None:
        transcript = """# Transcrição segmentada automática

## Proveniência

- Arquivo: `S01-L007.m4a`
- Modelo: `whisper-large-v3-turbo`
- Segmentos rejeitados: 29

## Transcrição

[00:01] O modelo B2B cresceu 40%."""
        self.assertEqual(validate_reference.normalized_numbers(transcript), {"40%"})

    def test_rejects_number_words_in_value_column(self) -> None:
        lesson = valid_lesson().replace(
            "**Conceito** — definição sustentada. [00:01–00:10]",
            """### Números e limites

| Papel | Item | Valor dito | Unidade/contexto | Evidência |
|---|---|---:|---|---|
| exemplo/evidência | comparação | quatro vezes | mais oportunidades | [00:01–00:10] |""",
        )
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any("number table value must use digits" in error for error in result["errors"])
        )

    def test_rejects_spoken_timestamp_as_technical_metadata_evidence(self) -> None:
        lesson = valid_lesson().replace(
            "**Conceito** — definição sustentada. [00:01–00:10]",
            """### Números e limites

| Papel | Item | Valor dito | Unidade/contexto | Evidência |
|---|---|---:|---|---|
| estrutura | segmentos ASR rejeitados | 55 | metadado técnico | [00:01–00:10] |""",
        )
        result = validate_reference.validate(lesson)
        self.assertTrue(
            any(
                "technical metadata must not cite spoken timestamp" in error
                for error in result["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
