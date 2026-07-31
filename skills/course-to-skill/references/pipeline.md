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

## Roteamento por capacidade

O pipeline usa papéis de capacidade, não nomes ou fornecedores específicos de modelos. Registrar no artefato de execução o papel usado, a versão/configuração disponível, o prompt ou regra aplicável, a entrada, a saída e o resultado dos gates. Não registrar segredos, mídia ou URLs temporárias.

| Etapa | Execução e papel permitido | Limite operacional |
| --- | --- | --- |
| Resolução de mídia, extração de áudio e ASR | Ferramentas locais e determinísticas | Não enviar mídia, áudio bruto ou credenciais a um modelo remoto para esta etapa. |
| Validação estrutural, timestamps, números, duplicação e placeholders | Scripts locais e determinísticos | O resultado do validador é obrigatório e não pode ser anulado por um modelo. |
| Limpeza mecânica em alto volume | Tier econômico | Formatação, segmentação, remoção de duplicação já detectada e normalização que não altere sentido. Não decidir fatos, preencher lacunas ou remover incertezas. |
| Revisão da transcrição e destilação | Tier balanceado | Comparar com a evidência disponível, preservar marcadores de incerteza, produzir referências com timestamps e separar conteúdo sustentado de `[derivado]`. |
| Auditoria, exceções e síntese final | Tier forte | Revisar apenas uma amostra definida, itens encaminhados pelos gates, conflitos e a síntese final. Não é o caminho padrão para todo o volume. |

Um artefato pode avançar somente depois da execução local obrigatória e dos gates aplicáveis. Se o tier econômico produzir alteração sem suporte mecânico claro, reverter para a entrada revisável e encaminhar ao tier balanceado ou à revisão humana. A seleção concreta de um modelo é uma configuração substituível fora desta política; escolher capacidades compatíveis com privacidade, custo, volume e idioma do curso.

## Revisão

Corrigir somente erros sustentados pelo áudio ou por grafia primária confirmada. Manter `[inaudível]`, `[?termo]`, `[ambíguo]`, `[referência visual perdida]` e `[lacuna de passos]` quando necessário.

## Destilação

Usar a transcrição revisada como única fonte semântica. Metadados curriculares podem preencher proveniência, mas não conteúdo. Separar afirmações sustentadas de aplicações editoriais marcadas como `[derivado]`.

## Publicação

Copiar somente referências validadas para a skill de conhecimento. A transcrição revisada permanece no corpus para auditoria; o áudio permanece em estado local ignorado. Atualizar o índice da skill depois da aprovação.
