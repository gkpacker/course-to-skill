# Contrato de adaptadores de mídia

Adaptadores conectam uma plataforma autorizada ao pipeline genérico. Eles não fazem parte da skill de conhecimento gerada.

## Entrada

- URL canônica da aula.
- Sessão autenticada já pertencente ao usuário.
- Destino local dentro de `state/`.

## Saída segura

- arquivo local de áudio ou vídeo;
- `media_id` não secreto, quando existir;
- duração e checksum;
- diagnóstico sanitizado, sem URL temporária ou cabeçalho sensível.

## Regras

1. Usar navegador somente para autenticação, navegação e descoberta autorizada.
2. Manter cookies, tokens, referers sensíveis e URLs assinadas em memória.
3. Entregar valores transitórios a processos locais por `stdin` ou descritor de arquivo; nunca por argumentos de processo, substituição de comando, variável impressa ou arquivo temporário versionável.
4. Não persistir respostas de API que contenham segredos.
5. Não contornar DRM, paywall ou limitação da plataforma.
6. Tratar expiração de URL como estado normal e resolver novamente quando autorizado.

O repositório genérico fornece o contrato, não adaptadores específicos de fornecedores. Um adaptador pode permanecer no repositório privado do curso.
