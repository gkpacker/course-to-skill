# Esquema do manifesto

## Curso

| Campo | Tipo | Regra |
|---|---|---|
| `course_id` | string | Identidade estável definida pelo projeto ou pela plataforma |
| `slug` | string | Slug usado em caminhos e nome da skill |
| `title` | string | Título oficial |
| `source` | string ou null | Host ou plataforma, sem credenciais |
| `default_language` | string | Código de idioma ou `auto` |

## Aula

| Campo | Tipo | Regra |
|---|---|---|
| `course_slug` | string | Deve corresponder ao curso |
| `section_id` | string ou integer | Identidade estável da seção |
| `section_order` | integer | Ordem curricular |
| `section_title` | string | Título oficial da seção |
| `lesson_id` | string ou integer | Identidade estável da aula na origem |
| `lesson_order` | integer | Ordem curricular global ou documentada |
| `artifact_id` | string | Código seguro para arquivos, por exemplo `S01-L003` |
| `title` | string | Título oficial da aula |
| `source_url` | string ou null | URL canônica sem credenciais |
| `media_type` | string | `audio`, `video`, `document`, `form` ou `none` |
| `media_id` | string ou null | Identificador não secreto |
| `duration_seconds` | integer ou null | Duração verificada |
| `status` | string | Estado atual do pipeline |
| `artifacts` | object | Caminhos relativos existentes |
| `review_flags` | array | Pendências materiais |
| `checksum` | string ou null | `sha256:<64 hex>` do áudio ou transcript de origem |

Nunca persistir cookies, API keys, tokens, query strings assinadas, cabeçalhos de autenticação ou URLs temporárias.

Uma aula `cataloged_non_media` pode ter `artifacts` vazio. Não apontar para transcrição ou referência inexistente.
