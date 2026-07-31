# Course to Skill

Turn authorized course material into an auditable corpus and a reusable Codex knowledge skill.

`course-to-skill` provides the generic pipeline, templates, and quality gates for processing a course without mixing raw evidence with the smaller skill that Codex eventually consumes. It is course- and provider-agnostic: private course content and platform-specific authentication stay in the repository created for that course.

> **Status:** private incubation. This repository contains no course corpus, provider credentials, signed media URLs, or vendor-specific authentication adapter. Nothing here automatically creates a remote repository, installs a skill, or publishes course content.

## Why this exists

A transcript alone is usually a poor skill: it is large, difficult to navigate, and easy to summarize beyond what the instructor actually said. This project keeps the source trail intact while producing smaller operational references.

```text
authorized media
        │
        ▼
raw ASR + timestamps ──► reviewed transcript ──► evidence-backed reference
        │                                                │
        └──────────── auditable corpus                   ▼
                                             validated Codex skill
```

The generated project separates:

- local media and transient state, which are always ignored by Git;
- raw and reviewed transcripts, retained as auditable evidence in private projects;
- distilled lesson references, accepted only after structural and evidence checks;
- a concise `SKILL.md` and index that route Codex to only the relevant references.

## What is included

- A Codex skill for operating the pipeline: [`skills/course-to-skill`](skills/course-to-skill/).
- A private/public-aware course repository initializer.
- Deterministic local audio normalization and Whisper transcription scripts.
- A capability-tier routing policy that keeps media, ASR, and deterministic validation local while reserving model use for the work that benefits from it.
- An evidence-first lesson template with timestamps, uncertainty markers, numeric checks, and clearly labeled derived applications.
- Validators and tests for generated references and repository policy.
- A provider adapter contract that keeps authentication outside the generic pipeline.

## Use it by asking Codex

The recommended interface is a conversation with Codex. You do not need to run the pipeline commands by hand unless you want to inspect or customize them.

First, ask Codex to install the operator skill:

> Install the `course-to-skill` skill from `gkpacker/course-to-skill`, path `skills/course-to-skill`.

Start a private course project with a prompt like:

> Use `$course-to-skill` to turn a course I am authorized to access into an auditable knowledge skill. The course is at `COURSE_URL`. Create a separate private repository, inventory the course before processing lessons, keep all media local and untracked, and do not publish or install the generated skill yet.

If the course requires an authenticated browser session, log in yourself and then tell the agent:

> I am logged in. Continue with `$course-to-skill`. Process the first representative lesson, show me the reviewed reference and validation result, and use it to calibrate the model routing before scaling to the rest of the course.

For an existing project, point Codex at the repository instead of starting over:

> Use `$course-to-skill` in `PATH_TO_COURSE_REPOSITORY`. Read its manifest and current status, validate the existing artifacts, then continue from the next incomplete lesson. Preserve raw ASR and do not redo validated lessons.

Other useful requests:

- **Audit quality:** “Audit the reviewed transcripts and generated references in `PATH`, report unsupported claims and missing numeric evidence, and do not rewrite them until I approve.”
- **Resume at scale:** “Continue the remaining lessons. Keep authenticated media capture serial, then parallelize independent review and sampled audit work where safe.”
- **Create a public-safe template:** “Create only a public-safe scaffold for this workflow. Do not include transcripts, generated references, provider adapters, course URLs, or private fixtures.”
- **Package the result:** “Package only validated references into the generated knowledge skill, update its problem-to-reference index, and show me how to install it. Do not publish it.”

When following these prompts, the agent should:

1. Read the `course-to-skill` skill and the target repository instructions before acting.
2. Confirm that the user is authorized to process the material and default the generated repository to private.
3. Inventory lessons and assign stable IDs before capturing media.
4. Keep course/provider-specific code and authenticated browser work in the private course repository, never in this generic repository.
5. Preserve raw ASR, produce a separate reviewed transcript, and distill only from the reviewed transcript.
6. Validate every reference and use a strong-model sampled audit before scaling a new routing configuration.
7. Keep media, credentials, cookies, signed URLs, and transient browser state out of Git and process arguments.
8. Report completed lessons, validation results, open uncertainty markers, and any login or access blocker.

The first representative lesson is intentionally a calibration run. After it passes both structural and semantic review, Codex can process additional lessons in batches without weakening the evidence trail.

## Requirements

- Python 3.11 or newer.
- [`ffmpeg`](https://ffmpeg.org/) and `ffprobe` for media processing.
- [`uv`](https://docs.astral.sh/uv/) to run optional Python dependencies without modifying the project environment.
- `mlx-whisper` for the current local transcription command (best suited to Apple Silicon). A different transcription backend can be introduced behind the same raw-output contract.
- GitHub CLI (`gh`) only if you later decide to create a remote repository.

## Quick start

Clone this repository and generate a separate repository for a course. Private is the default:

```bash
python3 skills/course-to-skill/scripts/init_course_repo.py \
  --title "Example Course" \
  --output ../example-course-skills \
  --visibility private \
  --github-owner OWNER
```

The initializer creates local files only. It prints the appropriate GitHub commands as a next step but never runs them.

The generated layout is:

```text
example-course-skills/
├── course.json
├── corpus/
│   ├── manifest/course.json
│   └── transcripts/
├── skills/
│   └── example-course/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── index.md
│           └── generated/
└── state/
    └── audio/
```

## Process a lesson

### 1. Inventory the lesson

Add a stable, non-secret lesson entry to `corpus/manifest/course.json`. Do not store cookies, bearer tokens, signed URLs, or authorization headers.

Provider-specific code may resolve authorized media, but it must pass only a local file and safe metadata into this pipeline. See the [provider adapter contract](skills/course-to-skill/references/provider-adapters.md).

### 2. Normalize local media

```bash
python3 skills/course-to-skill/scripts/extract_local_audio.py \
  --input /local/path/S01-L001.mp4 \
  --output state/audio/S01-L001.m4a
```

Remote URLs are rejected. The result is mono, 16 kHz audio suitable for speech recognition.

### 3. Transcribe with timestamps

```bash
uv run --python 3.13 --with mlx-whisper \
  python skills/course-to-skill/scripts/transcribe_media.py \
  --audio state/audio/S01-L001.m4a \
  --language auto \
  --json-output corpus/transcripts/S01-L001.json \
  --markdown-output corpus/transcripts/S01-L001.md
```

Keep the raw JSON unchanged. Review the Markdown against the audio and preserve uncertainty with the pipeline markers `[inaudível]`, `[?termo]`, `[ambíguo]`, `[referência visual perdida]`, and `[lacuna de passos]`.

### 4. Distill the reviewed transcript

Use the [lesson template](skills/course-to-skill/references/lesson-template.md) to create a reference in the generated skill. Material claims must point to timestamped evidence. Editorial applications must be marked as derived rather than presented as statements from the instructor.

### 5. Validate the reference

```bash
python3 skills/course-to-skill/scripts/validate_reference.py \
  --reference skills/example-course/references/generated/S01-L001.md \
  --transcript corpus/transcripts/S01-L001-reviewed.md \
  --strict-numbers
```

Only validated references should be added to the skill index. The detailed workflow and review thresholds are documented in [pipeline.md](skills/course-to-skill/references/pipeline.md) and [quality-gates.md](skills/course-to-skill/references/quality-gates.md).

## Model routing and calibration

The generic policy deliberately uses capability tiers instead of model names. Media handling, ASR, and structural validation run locally and deterministically. An economical tier may perform high-volume mechanical cleanup; a balanced tier handles evidence-aware review and distillation; a strong tier is reserved for sampled audits, exceptions, and final synthesis. Models never override deterministic validation or semantic quality gates.

Before changing a routing configuration or scaling it, run the documented A/B calibration protocol: change one variable at a time, evaluate the same representative sample, and require both structural and semantic gates to pass without a material fidelity regression. See [pipeline routing](skills/course-to-skill/references/pipeline.md) and [quality gates and calibration](skills/course-to-skill/references/quality-gates.md).

## Private and public repositories

### Private course repository

Private mode may version raw ASR, reviewed transcripts, and generated references. Audio, video, credentials, signed URLs, and transient state remain excluded.

```bash
python3 skills/course-to-skill/scripts/init_course_repo.py \
  --title "Example Course" \
  --output ../example-course-skills \
  --visibility private
```

### Public-safe scaffold

Public mode prepares infrastructure without assuming that course material can be redistributed. It ignores transcripts and generated lesson references by default.

```bash
python3 skills/course-to-skill/scripts/init_course_repo.py \
  --title "Example Course" \
  --output ../example-course-skills \
  --visibility public
```

Before creating a public remote, confirm redistribution rights, replace private fixtures, scan for secrets, and choose a code license. Follow the complete [repository visibility checklist](skills/course-to-skill/references/repository-visibility.md).

## Manual Codex installation

If you prefer the terminal, install only the operator skill directory:

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo gkpacker/course-to-skill \
  --path skills/course-to-skill
```

The skill is available from the next Codex turn after installation. The repository can also be developed and tested without installing the skill.

Installing this operator skill does not install a generated course skill. Creating a course repository also does not publish its contents or create a GitHub remote; those remain separate, explicit actions.

## Validation

Run the repository checks:

```bash
python3 -m unittest discover -s tests -v
uv run --with pyyaml \
  python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/course-to-skill
python3 -m compileall -q skills tests
git diff --check
```

The test suite covers private/public scaffold policy, safe local media handling, skill metadata, transcript structure, timestamps, numeric fidelity, uncertainty markers, and evidence requirements.

## Security and copyright boundary

- Process only material the user is authorized to access.
- Never bypass authentication, DRM, paywalls, or platform restrictions.
- Never persist credentials, cookies, authorization headers, or temporary media URLs.
- Never version raw audio or video.
- Do not publish transcripts, lesson references, slides, or other course material without explicit redistribution rights.
- Keep provider-specific adapters private until they receive a separate security and publication review.

## Project documentation

- [Pipeline states and artifact flow](skills/course-to-skill/references/pipeline.md)
- [Generated project layout](skills/course-to-skill/references/project-layout.md)
- [Course manifest schema](skills/course-to-skill/references/manifest-schema.md)
- [Lesson reference template](skills/course-to-skill/references/lesson-template.md)
- [Quality gates](skills/course-to-skill/references/quality-gates.md)
- [Provider adapter contract](skills/course-to-skill/references/provider-adapters.md)
- [Private/public repository policy](skills/course-to-skill/references/repository-visibility.md)

No license has been selected during private incubation. Choose and add one before making this repository public.
