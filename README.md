# Course to Skill

Turn authorized course material into an auditable corpus and an installable Codex knowledge skill.

This repository is in **private incubation**. It contains no course corpus, provider credentials, signed media URLs, or vendor-specific authentication adapter.

## Architecture

```text
authorized media
→ raw ASR
→ reviewed transcript
→ evidence-backed lesson reference
→ validated knowledge skill
```

The generated project keeps four layers separate:

- transient local media in ignored `state/`;
- raw and reviewed evidence in `corpus/`;
- validated knowledge in `skills/<course>/references/`;
- short routing instructions in `skills/<course>/SKILL.md`.

## Initialize a course repository

Private is the default:

```bash
python3 skills/course-to-skill/scripts/init_course_repo.py \
  --title "Example Course" \
  --output ../example-course-skills \
  --visibility private \
  --github-owner OWNER
```

To prepare a public-safe scaffold without publishing it:

```bash
python3 skills/course-to-skill/scripts/init_course_repo.py \
  --title "Example Course" \
  --output ../example-course-skills \
  --visibility public \
  --github-owner OWNER
```

Public mode ignores transcripts and generated lesson references until redistribution rights are confirmed. The initializer never creates a remote repository or publishes a skill.

See [repository visibility](skills/course-to-skill/references/repository-visibility.md) for the private/public GitHub commands and release checklist.

## Transcribe local media

```bash
uv run --python 3.13 --with mlx-whisper \
  python skills/course-to-skill/scripts/transcribe_media.py \
  --audio state/audio/S01-L001.m4a \
  --language auto \
  --json-output corpus/transcripts/S01-L001.json \
  --markdown-output corpus/transcripts/S01-L001.md
```

## Validate

```bash
python3 -m unittest discover -s tests -v
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/course-to-skill
```

## Security boundary

Provider-specific adapters belong in the private course repository until separately reviewed. They must not bypass authentication or DRM and must never persist credentials, cookies, authorization headers, or temporary media URLs.
