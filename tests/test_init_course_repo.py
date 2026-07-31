from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from _loader import load_script


init_course_repo = load_script("init_course_repo")


class InitCourseRepoTest(unittest.TestCase):
    def render(self, visibility: str) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        output = Path(temporary.name) / "curso-exemplo"
        values = {
            "__COURSE_TITLE__": "Curso Exemplo",
            "__COURSE_SLUG__": "curso-exemplo",
            "__VISIBILITY__": visibility,
            "__DEFAULT_LANGUAGE__": "pt",
            "__VERSION_TRANSCRIPTS__": "false" if visibility == "public" else "true",
            "__VERSION_REFERENCES__": "false" if visibility == "public" else "true",
            "__VISIBILITY_IGNORES__": (
                "corpus/transcripts/\nskills/curso-exemplo/references/generated/"
                if visibility == "public"
                else ""
            ),
        }
        template_root = (
            Path(init_course_repo.__file__).resolve().parents[1]
            / "assets"
            / "project-template"
        )
        init_course_repo.render_tree(template_root, output, values)
        return output

    def test_slugify_is_stable_and_ascii(self) -> None:
        self.assertEqual(init_course_repo.slugify("Estratégia & Ação"), "estrategia-acao")

    def test_private_scaffold_versions_reviewed_content(self) -> None:
        output = self.render("private")
        config = json.loads((output / "course.json").read_text(encoding="utf-8"))
        self.assertTrue(config["repository"]["version_transcripts"])
        self.assertTrue(config["repository"]["version_generated_references"])
        self.assertTrue((output / "skills/curso-exemplo/SKILL.md").is_file())
        subprocess.run(
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=output,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_scaffold_contains_operational_model_routing_policy(self) -> None:
        output = self.render("private")
        instructions = (output / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Model routing", instructions)
        self.assertIn("ASR, and structural validation local and deterministic", instructions)
        self.assertIn("one variable changed at a time", instructions)
        self.assertIn("semantic quality gate", instructions)

    def test_public_scaffold_excludes_course_content_by_default(self) -> None:
        output = self.render("public")
        config = json.loads((output / "course.json").read_text(encoding="utf-8"))
        ignore = (output / ".gitignore").read_text(encoding="utf-8")
        self.assertFalse(config["repository"]["version_transcripts"])
        self.assertFalse(config["repository"]["version_generated_references"])
        self.assertIn("corpus/transcripts/", ignore)
        self.assertIn("skills/curso-exemplo/references/generated/", ignore)

    def test_refuses_to_write_into_nonempty_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "existing.txt").write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                init_course_repo.render_tree(output, output, {})


if __name__ == "__main__":
    unittest.main()
