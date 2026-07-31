from __future__ import annotations

import unittest
from pathlib import Path

from _loader import load_script


extract_local_audio = load_script("extract_local_audio")


class ExtractLocalAudioTest(unittest.TestCase):
    def test_rejects_remote_or_signed_input(self) -> None:
        with self.assertRaises(ValueError):
            extract_local_audio.require_local_path("https://example.com/media.m3u8?token=x")

    def test_builds_quiet_mono_audio_command(self) -> None:
        command = extract_local_audio.build_ffmpeg_command(
            Path("lesson.mp4"), Path("state/audio/S01-L001.m4a")
        )
        self.assertEqual(command[0], "ffmpeg")
        self.assertIn("-vn", command)
        self.assertIn("16000", command)
        self.assertEqual(command[-1], "state/audio/S01-L001.m4a")


if __name__ == "__main__":
    unittest.main()
