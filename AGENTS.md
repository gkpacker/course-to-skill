# AGENTS.md

## Scope

- Keep this repository course- and provider-agnostic.
- Do not add private course transcripts, lesson references, URLs, IDs, names, or fixtures.
- Use only synthetic fixtures created for this repository.

## Architecture

- Keep deterministic operations in `skills/course-to-skill/scripts/`.
- Keep detailed policies and schemas in `skills/course-to-skill/references/`.
- Keep generated project templates in `skills/course-to-skill/assets/`.
- Keep `SKILL.md` concise and route to references progressively.

## Safety

- Default generated course repositories to private.
- Never persist credentials, cookies, signed URLs, authorization headers, audio, or video.
- Never implement DRM, paywall, or authentication bypass.
- Do not make this repository public without explicit user approval and a clean public-release audit.

## Verification

- Run `python3 -m unittest discover -s tests -v`.
- Run `quick_validate.py skills/course-to-skill` with PyYAML available.
- Run `python3 -m compileall -q skills tests` and `git diff --check`.
- Scan tracked content for secrets before every push.
