# Prompt Cursor + OpenSpec

Use este prompt no Cursor para iniciar uma mudanca OpenSpec voltada ao merge de duas Angular Libraries em uma unica biblioteca.

```text
/opsx:new merge-duas-angular-libraries

Quero criar uma spec OpenSpec para fazer o merge de duas Angular Libraries existentes em uma unica library Angular publicavel.

Contexto:
- Existem duas Angular Libraries no projeto.
- Os componentes, diretivas e servicos publicos dessas libraries nao conflitam entre si.
- Os conflitos esperados estao principalmente nos arquivos base do Angular e do empacotamento, como angular.json, tsconfig, package.json, ng-package.json, public-api.ts, configuracoes de teste, estilos base e assets.

Objetivo:
Criar uma library final chamada @minha-org/ui, consolidando os componentes das duas libraries sem quebrar as APIs publicas existentes.

Requisitos principais:
- Inventariar as duas libraries atuais.
- Identificar todos os entry points, exports publicos, componentes, diretivas, pipes, servicos, tokens e estilos.
- Criar ou escolher uma library alvo para receber os artefatos das duas libraries.
- Consolidar arquivos base do Angular sem duplicacao desnecessaria.
- Preservar imports publicos sempre que possivel.
- Criar estrategia de compatibilidade ou aliases temporarios quando houver consumidores existentes.
- Resolver conflitos somente em arquivos estruturais/base.
- Nao alterar comportamento visual ou funcional dos componentes.
- Manter a migracao incremental e validavel por build/testes.

Antes de implementar, gere proposal.md, design.md, specs e tasks.md.

Use estes arquivos como referencia:
@sdd-angular-library-merge-example/sdd-angular-library-merge.md
@spec-driven-development-angular.md

Inclua no design:
- inventario esperado das duas libraries
- criterio para escolher a library alvo
- estrategia de merge dos arquivos base Angular
- estrategia para public-api.ts e secondary entry points
- estrategia para package.json, peerDependencies e dependencies
- estrategia para tsconfig paths
- estrategia para estilos, temas e assets
- plano de migracao dos imports
- plano de validacao por build/testes
- riscos e rollback

Nao implemente codigo ainda.
Crie apenas a estrutura OpenSpec da mudanca.
```

## Prompt de Implementacao Apos Revisao

Use somente depois que `proposal.md`, `design.md`, `specs/` e `tasks.md` estiverem revisados.

```text
/opsx:apply

Implemente apenas as tasks aprovadas em @openspec/changes/merge-duas-angular-libraries/tasks.md.

Comece pelo inventario das duas libraries e pela definicao da library alvo.
Nao mova todos os componentes de uma vez.

Depois de cada etapa:
- atualize tasks.md
- rode build/testes relevantes
- reporte arquivos alterados
- pare antes da proxima etapa de migracao
```

## Referencias Locais Recomendadas

Ao usar no Cursor, referencie tambem:

```text
@sdd-angular-library-merge-example/sdd-angular-library-merge.md
@spec-driven-development-angular.md
@openspec/changes/merge-duas-angular-libraries/tasks.md
@openspec/changes/merge-duas-angular-libraries/design.md
@openspec/changes/merge-duas-angular-libraries/specs/
```
