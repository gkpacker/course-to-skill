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

## Gates semânticos

O validador estrutural é necessário, mas não suficiente. Antes de aprovar uma referência, executar gates semânticos sobre uma amostra representativa e todos os itens encaminhados para exceção:

- **Fidelidade à evidência:** cada afirmação material, ordem de procedimento e número corresponde à passagem indicada; não há conteúdo externo ou lacuna preenchida por inferência.
- **Preservação de incerteza:** marcadores de dúvida, trechos inaudíveis e referências visuais perdidas permanecem até haver evidência registrada para corrigi-los.
- **Atribuição e modalidade:** hipótese, exemplo, opinião, regra e aplicação editorial mantêm seu status; `[derivado]` não é apresentado como fala do instrutor.
- **Completude operacional:** uma instrução publicada contém os pré-requisitos e passos que a evidência sustenta, ou explicita a lacuna em vez de inventar a transição.
- **Utilidade de recuperação:** título, índice e essência operacional permitem encontrar a referência para o problema correto sem ampliar seu escopo.

Falha em qualquer gate semântico retorna o item a `reviewed` ou `distilled`, conforme a origem da falha. Dúvida material continua sendo caso de revisão humana.

## Calibração A/B de roteamento

Calibrar a política antes de ampliar volume ou trocar configuração. Usar um conjunto sintético ou autorizado, com amostra estratificada por idioma, qualidade de áudio, densidade numérica, vocabulário técnico e presença de lacunas. Preservar entradas, saídas e decisões de revisão para auditoria, sem versionar mídia ou segredos.

1. Definir uma linha de base e métricas: aprovação estrutural, aprovação semântica, taxa de encaminhamento humano, alterações sem suporte, tempo por aula e custo por aula.
2. Alterar **uma variável por experimento**: papel/capacidade, prompt, tamanho do lote, regra de encaminhamento, temperatura ou estratégia de amostragem. Manter corpus, avaliadores, gates e as demais configurações constantes.
3. Executar A e B na mesma amostra, com ordem aleatorizada quando houver revisão humana. Avaliadores devem ver a evidência e aplicar a mesma rubrica, sem saber qual variante produziu a saída quando isso for viável.
4. Comparar as métricas e investigar toda regressão de fidelidade, incerteza, atribuição ou números, mesmo que custo ou velocidade melhorem.
5. Promover uma variante somente se passar os gates estruturais e semânticos sem regressão material; registrar a decisão, a única variável alterada, o tamanho da amostra e as exceções observadas. Caso contrário, manter a linha de base ou encaminhar o caso ao tier superior ou à revisão humana.

## Critérios de aprovação

- Zero informação externa apresentada como conteúdo da aula.
- Todos os números falados preservados.
- Procedimentos mantêm ordem e lacunas.
- Regras, heurísticas e opiniões explícitas classificadas sem causalidade inventada.
- Afirmações materiais possuem evidência temporal suficiente.
- Aplicações derivadas estão separadas e rotuladas.
- Timestamps apontam para passagens existentes e não excedem a duração.
- Lacunas permanecem explícitas.
- A política de roteamento foi aplicada sem usar um modelo para anular validação determinística ou gate semântico.
