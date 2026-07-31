# Controles de qualidade

## Bloqueios automáticos

- Segmento com timestamp posterior à duração do áudio.
- Bloco obrigatório ausente.
- Placeholder `TODO` ou texto de scaffold presente.
- Essência operacional sem bullets, com mais de 3 bullets ou sem evidência temporal.
- Aplicação editorial sem marcador `[derivado]` e evidência temporal.
- Número falado ausente do registro de números e limites.
- Valor escrito por extenso na coluna `Valor dito`, impedindo comparação automática.
- Marcador de incerteza removido sem revisão registrada.
- Conteúdo duplicado no fim do ASR.
- Credencial ou URL assinada em qualquer artefato versionado.
- Causalidade artificial expressa como `PORQUE não informado`.

## Revisão humana

Encaminhar para revisão quando houver:

- `[inaudível]`, `[?termo]` ou `[ambíguo]` material para a técnica.
- Número com unidade incerta.
- Referência visual que interrompe um procedimento.
- Duas transcrições divergentes de um mesmo trecho.
- Nome de marca, pessoa, ferramenta ou produto sem grafia confirmável pelo áudio.
- Causalidade necessária para uma regra, mas não falada.
- Afirmação material cujo timestamp não contém suporte suficiente.
- Timestamp de fala usado como evidência para metadado técnico ou curricular não pronunciado no áudio.
- Contagem editorial apresentada como número dito pelo instrutor.
- Generalização editorial apresentada como conteúdo do instrutor.

## Critérios de aprovação

- Zero informação externa apresentada como conteúdo da aula.
- Todos os números falados preservados.
- Procedimentos mantêm ordem e lacunas.
- Regras, heurísticas e opiniões explícitas classificadas sem causalidade inventada.
- Afirmações materiais possuem evidência temporal suficiente.
- Aplicações derivadas estão separadas e rotuladas.
- Timestamps apontam para passagens existentes e não excedem a duração.
- Lacunas permanecem explícitas.
