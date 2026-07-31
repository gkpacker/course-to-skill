from __future__ import annotations

import unittest
from pathlib import Path

from _loader import load_script

transcribe_media = load_script("transcribe_media")


class TranscribeMediaTest(unittest.TestCase):
    def test_formats_short_and_long_timestamps(self) -> None:
        self.assertEqual(transcribe_media.format_timestamp(65.9), "01:05")
        self.assertEqual(transcribe_media.format_timestamp(3661), "01:01:01")

    def test_rejects_segments_at_duration_and_duplicates(self) -> None:
        segments = [
            {"start": 0, "end": 2, "text": " Primeiro trecho. "},
            {"start": 2, "end": 4, "text": "Primeiro trecho."},
            {"start": 4, "end": 6, "text": "Segundo trecho."},
            {"start": 10, "end": 12, "text": "Alucinação final."},
        ]
        accepted, rejected = transcribe_media.sanitize_segments(segments, 10)
        self.assertEqual([item["text"] for item in accepted], ["Primeiro trecho.", "Segundo trecho."])
        self.assertEqual(
            [item["reason"] for item in rejected],
            ["consecutive_duplicate", "starts_at_or_after_duration"],
        )

    def test_renders_auditable_markdown(self) -> None:
        markdown = transcribe_media.render_markdown(
            Path("lesson.m4a"),
            "test-model",
            65,
            [{"start": 1, "end": 2, "text": "Conteúdo."}],
            [{"reason": "empty", "segment": {}}],
        )
        self.assertIn("- Duração: 01:05", markdown)
        self.assertIn("Segmentos rejeitados automaticamente: 1", markdown)
        self.assertIn("[00:01] Conteúdo.", markdown)


if __name__ == "__main__":
    unittest.main()
