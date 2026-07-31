# Template de destilação v2

Separar duas camadas no mesmo documento:

1. **Conteúdo sustentado:** afirmações recuperáveis do áudio, sempre rastreáveis por timestamp.
2. **Aplicação editorial:** inferências úteis para roteamento da skill, sempre marcadas como `[derivado]`.

Não preencher uma grade fixa só para manter simetria. O núcleo abaixo é obrigatório; os blocos de conteúdo são condicionais ao tipo da aula.

## Núcleo obrigatório

### `## Proveniência e estado`

Registrar:

- curso, fase, ordem e `lesson_id`;
- título e origem: `portal`, `declarado no áudio` ou `[inferido]`;
- artefato de transcrição, duração e escopo da fonte;
- estado da transcrição e da destilação;
- tipo: `conceitual`, `procedural`, `estudo de caso` ou `misto`;
- cobertura: `completa` ou `parcial`;
- marcadores de incerteza ainda abertos.

Nunca incluir credenciais, query strings do player ou URLs assinadas.

Metadados curriculares do portal podem preencher curso, fase, ordem, `lesson_id` e título. Eles devem ser identificados como metadados e não autorizam completar o conteúdo semântico da aula. Um título operacional inferido pode ser explicado à parte, mas o título principal deve permanecer alinhado ao inventário oficial.

### `## Essência operacional`

Usar de 1 a 3 bullets. Cada bullet deve:

- começar com `[decisão]`, `[ação]` ou `[modelo]`;
- descrever somente uma capacidade sustentada pela aula;
- terminar com timestamp ou intervalo, por exemplo `[04:31–05:32]`.

Não prometer domínio de algo que a aula apenas anuncia para vídeos seguintes.

### `## Conteúdo sustentado`

Incluir somente os blocos aplicáveis descritos abaixo. Associar cada afirmação material ao menor intervalo de áudio que a sustenta.

### `## Aplicação editorial`

Traduzir o conteúdo em gatilhos úteis para um agente sem atribuí-los ao instrutor. Organizar conforme necessário em `Problemas que aciona`, `Entradas necessárias`, `Saídas possíveis` e `Não usar quando`.

Todo bullet desta seção deve começar com `[derivado]` e terminar com timestamp ou intervalo. O timestamp aponta para o conteúdo que torna a inferência razoável.

### `## Lacunas e revisão`

Registrar trecho, marcador, impacto operacional, ação de revisão e se a pendência bloqueia publicação. Incluir também passos, causas, critérios ou contraindicações não ensinados.

## Blocos condicionais de conteúdo

### Conceitos e distinções

Usar quando o curso definir um termo ou separar conceitos confundidos. Formato:

```text
**Termo** — definição fiel. Consequência prática explicitamente sustentada. [02:24–03:20]
```

Não acrescentar consequência prática quando ela não for dita.

### Procedimentos

Usar somente quando houver sequência de ações. Manter ordem, uma ação por passo e timestamps. Marcar `[lacuna de passos]` ou `[referência visual perdida]` no ponto exato. Registrar `Resultado esperado` apenas quando descrito no áudio.

Omitir este bloco em aula conceitual; não escrever boilerplate como “nenhum procedimento”.

### Regras e critérios de decisão

Classificar como `[regra explícita]`, `[heurística explícita]` ou `[opinião explícita]`. Usar `SE/ENTÃO/PORQUE` somente quando situação, ação e razão forem sustentadas. Se a razão não for falada, omitir `PORQUE` e registrar a causalidade como lacuna.

Nunca escrever `PORQUE não informado` e nunca elevar uma síntese editorial a regra do curso.

### Exemplos e evidências

Separar exemplos de parâmetros operacionais. Registrar contexto, contraste e ponto demonstrado, sem generalizar além da conclusão falada.

### Números e limites

Preservar todo número falado e classificá-lo pelo papel que exerce:

| Papel | Exemplos |
|---|---|
| parâmetro operacional | limite, faixa, duração ou valor usado para executar |
| exemplo/evidência | preço, comparação ou resultado usado para sustentar um ponto |
| credencial/contexto | tempo de experiência, tamanho ou outro dado contextual |
| estrutura | quantidade de etapas, perspectivas ou categorias |

Usar a tabela `Papel | Item | Valor dito | Unidade/contexto | Evidência`. Nunca tratar automaticamente um preço de exemplo como recomendação ou parâmetro.

Normalizar números falados para algarismos: `vinte por cento` → `20%`, `quatro vezes` → `4x`. Preservar a unidade dita. Usar `[unidade não informada]` quando necessário e `[?25]` quando o valor for acusticamente incerto.

Não colocar nessa tabela números que existam apenas em metadados técnicos, como versão do modelo, quantidade de segmentos ASR ou ordem curricular. Não apresentar uma contagem editorial como `Valor dito` quando o áudio apenas enumera itens sem verbalizar o total.

### Diagnóstico e falhas

Registrar somente os componentes sustentados entre `Sintoma`, `Causa` e `Correção`. Não exigir a tríade completa. Ausência de causa não autoriza deduzi-la.

## Convenções de evidência

- Usar `[MM:SS]` para um ponto e `[MM:SS–MM:SS]` para um intervalo.
- Preferir o menor intervalo que sustenta a afirmação completa.
- Manter `[inaudível]`, `[?termo]`, `[ambíguo]`, `[referência visual perdida]` e `[lacuna de passos]` junto à afirmação afetada.
- Marcar normalização de grafia confirmada no registro de revisão; não remover incerteza silenciosamente.
- Não copiar a transcrição inteira. A destilação deve permanecer verificável sem duplicar a camada bruta.
