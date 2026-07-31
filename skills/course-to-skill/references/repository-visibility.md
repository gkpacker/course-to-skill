# Visibilidade do repositório

## Regra padrão

Criar projetos de curso como **privados**. Tornar público somente depois de confirmar direitos de redistribuição sobre código, transcripts, referências, exemplos, imagens e materiais complementares.

## Configuração privada

O scaffold privado permite versionar ASR, transcrições revisadas e referências, mas continua ignorando áudio, vídeo, modelos e estado transitório.

Depois de revisar o diretório local:

```bash
git init -b main
git add .
git commit -m "Initialize course skill"
gh repo create OWNER/REPOSITORY --private --source . --remote origin --push
```

## Configuração pública

O scaffold público ignora por padrão `corpus/transcripts/` e referências geradas. Ele publica apenas infraestrutura e templates até que o titular confirme direitos sobre o conteúdo.

Checklist antes de criar o remoto:

1. Executar a varredura de segredos.
2. Confirmar que não há mídia ou URLs assinadas.
3. Substituir exemplos privados por fixtures sintéticas ou de domínio público.
4. Escolher uma licença para o código.
5. Confirmar por escrito que o conteúdo versionado pode ser redistribuído.

Somente depois da confirmação:

```bash
git init -b main
git add .
git commit -m "Initialize course skill"
gh repo create OWNER/REPOSITORY --public --source . --remote origin --push
```

Criar um repositório público é uma ação externa separada de gerar a skill local. O scaffold nunca executa esses comandos automaticamente.
