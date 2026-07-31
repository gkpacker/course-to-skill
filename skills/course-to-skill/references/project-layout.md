# Layout do projeto gerado

```text
course-skills/
├── course.json
├── corpus/
│   ├── manifest/course.json
│   └── transcripts/
├── skills/
│   └── course-knowledge/
│       ├── SKILL.md
│       ├── agents/openai.yaml
│       └── references/
│           ├── index.md
│           └── generated/
└── state/
    └── audio/
```

## Camadas

- `course.json`: política do projeto, idioma e visibilidade pretendida.
- `corpus/manifest/`: inventário e estado do pipeline.
- `corpus/transcripts/`: ASR bruto e transcrição revisada para auditoria.
- `skills/*/references/generated/`: destilações validadas; ignoradas por padrão no modo público.
- `skills/*/references/index.md`: mapa consultável das referências aprovadas.
- `state/`: áudio, vídeo e estado temporário ignorados pelo Git.

A skill instalada deve permanecer pequena. Carregar primeiro `references/index.md` e depois somente as referências necessárias para a pergunta.
