---
name: course-to-skill
description: Initialize and operate an auditable pipeline that turns authorized course media into reviewed transcripts, evidence-backed references, and an installable Codex knowledge skill. Use when Codex needs to scaffold a private or public course repository, inventory lessons, transcribe local audio or video with Whisper, review ASR, distill lessons with timestamps, validate references, or package validated knowledge without bundling raw media.
---

# Course to Skill

Construir uma skill de conhecimento a partir de material de curso autorizado, mantendo separadas a evidência auditável e a camada operacional instalada.

## Escolher a operação

- **Inicializar um projeto:** ler [repository-visibility.md](references/repository-visibility.md) e executar `scripts/init_course_repo.py`.
- **Inventariar ou processar aulas:** ler [pipeline.md](references/pipeline.md), [manifest-schema.md](references/manifest-schema.md) e [provider-adapters.md](references/provider-adapters.md).
- **Revisar e destilar:** ler [pipeline.md](references/pipeline.md), [lesson-template.md](references/lesson-template.md) e [quality-gates.md](references/quality-gates.md).
- **Organizar o resultado:** usar [project-layout.md](references/project-layout.md).

## Processar uma aula

1. Confirmar que o usuário possui acesso e autorização para processar o material.
2. Registrar a aula no manifesto sem cookies, tokens, URLs assinadas ou cabeçalhos de autenticação.
3. Resolver a mídia por um adaptador autorizado e manter credenciais somente em memória.
4. Converter a mídia para um arquivo local de áudio quando necessário.
5. Transcrever com `scripts/transcribe_media.py`, preservando o JSON bruto antes de qualquer correção.
6. Criar uma transcrição revisada sem completar conteúdo ausente.
7. Destilar exclusivamente a partir da transcrição revisada.
8. Validar com `scripts/validate_reference.py --strict-numbers`.
9. Copiar somente referências aprovadas para a skill de conhecimento gerada.
10. Atualizar o índice `problema → referência` e o estado do manifesto.

## Roteamento de modelos

Aplicar a política em [pipeline.md](references/pipeline.md): mídia, ASR e validação determinística permanecem locais; usar o tier econômico somente para limpeza mecânica de alto volume, o tier balanceado para revisão e destilação, e o tier forte para auditoria amostral, exceções e síntese final. Não substituir os gates estruturais e semânticos por julgamento do modelo. Calibrar alterações seguindo o protocolo A/B em [quality-gates.md](references/quality-gates.md).

## Inicializar um repositório de curso

Privado por padrão:

```bash
python3 scripts/init_course_repo.py \
  --title "Nome do curso" \
  --output /caminho/curso-skills \
  --visibility private
```

Para preparar um repositório público sem publicar conteúdo do curso:

```bash
python3 scripts/init_course_repo.py \
  --title "Nome do curso" \
  --output /caminho/curso-skills \
  --visibility public
```

O scaffold não cria nem publica um repositório remoto. Seguir o checklist emitido pelo comando e confirmar novamente antes de qualquer criação pública no GitHub.

## Transcrever mídia local

Normalizar vídeo ou áudio local:

```bash
python3 scripts/extract_local_audio.py \
  --input state/media/S01-L001.mp4 \
  --output state/audio/S01-L001.m4a
```

Transcrever:

```bash
uv run --python 3.13 --with mlx-whisper \
  python scripts/transcribe_media.py \
  --audio state/audio/S01-L001.m4a \
  --language pt \
  --json-output corpus/transcripts/S01-L001.json \
  --markdown-output corpus/transcripts/S01-L001.md
```

## Validar uma referência

```bash
python3 scripts/validate_reference.py \
  --reference skills/course-knowledge/references/S01-L001.md \
  --transcript corpus/transcripts/S01-L001-reviewed.md \
  --strict-numbers
```

## Restrições

- Não contornar autenticação, DRM, paywall ou limitação técnica da plataforma.
- Não publicar conteúdo de curso sem direitos explícitos para redistribuição.
- Não versionar áudio, vídeo, modelos, cookies, tokens, URLs assinadas ou estado transitório.
- Não usar material visual para completar silenciosamente uma lacuna do áudio.
- Não transformar exemplo, opinião ou síntese editorial em regra objetiva do instrutor.
- Não instalar ou publicar a skill gerada sem pedido explícito.
