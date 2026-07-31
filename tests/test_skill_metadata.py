from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillMetadataTest(unittest.TestCase):
    def test_skill_frontmatter_is_complete(self) -> None:
        text = (
            ROOT / "skills" / "course-to-skill" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: course-to-skill\n"))
        self.assertIn("\ndescription:", text)
        self.assertNotIn("[TODO", text)

    def test_interface_prompt_mentions_skill(self) -> None:
        text = (
            ROOT / "skills" / "course-to-skill" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("$course-to-skill", text)


if __name__ == "__main__":
    unittest.main()
