# Fluxo OpenSpec + Cursor

Este fluxo usa o OpenSpec para criar e manter a estrutura oficial da mudanca, enquanto o Cursor executa o merge das Angular Libraries com base nos arquivos gerados.

## 1. Criar a Mudanca

No Cursor:

```text
/opsx:new merge-duas-angular-libraries
```

Depois cole:

```text
Quero criar uma spec OpenSpec para fazer o merge de duas Angular Libraries existentes em uma unica library Angular publicavel.

Contexto:
- Existem duas Angular Libraries no projeto.
- Os componentes, diretivas, pipes e servicos publicos nao conflitam entre si.
- Os conflitos esperados estao nos arquivos base do Angular e empacotamento.

A library final deve se chamar @minha-org/ui.

Requisitos principais:
- Inventariar as duas libraries atuais.
- Escolher uma library alvo ou criar uma nova library limpa.
- Consolidar angular.json, tsconfig, package.json, ng-package.json, public-api.ts, configuracoes de teste, estilos base e assets.
- Preservar APIs publicas sempre que possivel.
- Manter estrategia de compatibilidade para imports antigos se necessario.
- Migrar em lotes pequenos e validaveis.
- Nao alterar comportamento visual ou funcional dos componentes.
- Nao remover as libraries antigas ate confirmar que nao existem consumidores ativos.

Use estes arquivos como referencia:
@sdd-angular-library-merge-example/sdd-angular-library-merge.md
@spec-driven-development-angular.md

Nao implemente codigo ainda.
Crie apenas a estrutura OpenSpec da mudanca.
```

## 2. Gerar Proposal, Design, Specs e Tasks

No Cursor:

```text
/opsx:ff
```

Prompt complementar recomendado:

```text
/opsx:ff

Gere os arquivos da mudanca OpenSpec:
- proposal.md
- design.md
- tasks.md
- specs/

Aplique a estrutura do SDD referenciado, mas adapte ao codigo real deste projeto.

Em tasks.md, quebre a implementacao em etapas pequenas:
1. inventario das duas libraries
2. comparacao de exports publicos
3. comparacao de dependencias
4. escolha da library alvo
5. consolidacao dos arquivos base Angular
6. migracao de um lote pequeno da primeira library
7. migracao de um lote pequeno da segunda library
8. atualizacao de imports consumidores
9. validacao de build/testes
10. remocao ou deprecacao das libraries antigas

Nao implemente codigo ainda.
```

Estrutura esperada:

```text
openspec/
  changes/
    merge-duas-angular-libraries/
      proposal.md
      design.md
      tasks.md
      specs/
```

## 3. Revisar a Mudanca Antes de Implementar

No Cursor:

```text
Revise a mudanca OpenSpec criada em:
@openspec/changes/merge-duas-angular-libraries/proposal.md
@openspec/changes/merge-duas-angular-libraries/design.md
@openspec/changes/merge-duas-angular-libraries/tasks.md
@openspec/changes/merge-duas-angular-libraries/specs/

Verifique se:
- o inventario das duas libraries esta previsto
- a escolha da library alvo esta justificada
- os arquivos base conflitantes estao listados
- a estrategia para public-api.ts esta clara
- a estrategia para tsconfig paths esta clara
- a estrategia de compatibilidade esta definida
- as tasks estao pequenas o suficiente
- nao ha remocao prematura das libraries antigas

Nao implemente ainda. Apenas aponte ajustes necessarios.
```

## 4. Ajustar a Spec Quando Necessario

Use este prompt se a revisao encontrar lacunas:

```text
Atualize a mudanca OpenSpec com estes ajustes:

- Antes de mover arquivos, gerar inventario dos exports publicos das duas libraries.
- A library alvo deve ser escolhida por criterio tecnico documentado.
- Imports antigos devem continuar funcionando por alias temporario ou wrapper quando houver consumidores ativos.
- Nao remover nenhuma library antiga ate uma busca global confirmar ausencia de imports.
- Qualquer mudanca em public-api.ts deve preservar ou documentar breaking changes.
- Consolidar arquivos base do Angular antes de migrar componentes em massa.

Atualize proposal.md, design.md, tasks.md e specs conforme necessario.
Nao implemente codigo.
```

## 5. Implementar Somente Depois da Revisao

No Cursor:

```text
/opsx:apply

Implemente apenas a primeira etapa de @openspec/changes/merge-duas-angular-libraries/tasks.md.

Pare apos:
- inventariar as duas libraries
- listar exports publicos
- listar entry points
- listar dependencias e peerDependencies
- identificar arquivos base conflitantes
- atualizar tasks.md com o resultado do inventario

Nao mova componentes ainda.
```

## 6. Consolidar Arquivos Base

Depois do inventario revisado:

```text
/opsx:apply

Continue seguindo @openspec/changes/merge-duas-angular-libraries/tasks.md.

Execute somente a etapa de consolidacao dos arquivos base:
- angular.json
- tsconfig*.json
- package.json
- ng-package.json
- public-api.ts inicial
- configuracoes de teste/build
- estilos base/assets compartilhados

Nao remova as libraries antigas ainda.
Depois rode build/testes relevantes e atualize tasks.md.
```

## 7. Migrar em Lotes Pequenos

Para cada lote:

```text
/opsx:apply

Migre apenas o proximo lote pequeno definido em @openspec/changes/merge-duas-angular-libraries/tasks.md.

Antes de editar:
- confirme se os componentes do lote nao conflitam
- confirme dependencias internas
- confirme exports publicos esperados

Depois de editar:
- rode build/testes relevantes
- atualize tasks.md
- reporte imports antigos ainda existentes
- pare antes do proximo lote
```

## 8. Finalizar e Arquivar

Somente depois que todos os criterios de aceite estiverem validados:

```text
/opsx:archive
```

Antes de arquivar, confirme:

- `proposal.md` reflete o que foi entregue.
- `design.md` esta atualizado com decisoes reais.
- `tasks.md` esta completo.
- `specs/` contem os requisitos finais.
- build e testes relevantes passaram.
- nao ha imports ativos para libraries antigas, ou eles estao cobertos por estrategia de compatibilidade.

## Regra Principal

Os arquivos deste diretorio sao entrada e referencia.

A fonte oficial da mudanca deve ser gerada e mantida pelo OpenSpec em:

```text
openspec/changes/merge-duas-angular-libraries/
```

O Cursor deve implementar codigo somente depois que `proposal.md`, `design.md`, `tasks.md` e `specs/` estiverem revisados.
