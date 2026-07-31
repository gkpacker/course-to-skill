# Pipeline de ingestão

## Estados

```text
discovered
→ media_resolved
→ audio_extracted
→ transcribed
→ reviewed
→ distilled
→ validated
→ published
```

Itens sem áudio ou vídeo seguem `discovered → cataloged_non_media`. Não fabricar transcrição ou timestamps para formulários, PDFs ou atividades. Criar uma referência somente quando o conteúdo daquele meio tiver sido capturado e revisado com evidência apropriada.

Registrar o estado atual no manifesto. Repetir uma etapa deve produzir o mesmo artefato ou substituir somente o artefato daquela etapa.

## Inventário

Catalogar `curso → seção → módulo opcional → aula`. Usar o ID estável da plataforma como `lesson_id` e um `artifact_id` curricular como `S01-L003` para nomear arquivos. Guardar apenas URLs públicas ou canônicas sem credenciais.

## Mídia

Obter mídia somente por acesso autorizado. O adaptador pode resolver uma URL temporária em memória, mas deve entregar ao pipeline apenas o arquivo local, um identificador não secreto e metadados seguros. Consultar [provider-adapters.md](provider-adapters.md).

## Transcrição

Executar Whisper localmente com timestamps. Preservar o JSON bruto antes de gerar Markdown e rejeitar segmentos vazios, duplicados ou iniciados no fim do arquivo.

## Revisão

Corrigir somente erros sustentados pelo áudio ou por grafia primária confirmada. Manter `[inaudível]`, `[?termo]`, `[ambíguo]`, `[referência visual perdida]` e `[lacuna de passos]` quando necessário.

## Destilação

Usar a transcrição revisada como única fonte semântica. Metadados curriculares podem preencher proveniência, mas não conteúdo. Separar afirmações sustentadas de aplicações editoriais marcadas como `[derivado]`.

## Publicação

Copiar somente referências validadas para a skill de conhecimento. A transcrição revisada permanece no corpus para auditoria; o áudio permanece em estado local ignorado. Atualizar o índice da skill depois da aprovação.
