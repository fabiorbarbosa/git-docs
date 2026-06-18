# Fluxo OpenSpec + Cursor

Este fluxo usa o OpenSpec para criar e manter a estrutura oficial da mudanca, enquanto o Cursor executa a implementacao com base nos arquivos gerados.

## 1. Criar a Mudanca

No Cursor:

```text
/opsx:new extrair-ui-components-para-angular-library
```

Depois cole:

```text
Quero criar uma spec OpenSpec para extrair os componentes UI deste projeto Angular para uma nova biblioteca Angular publicavel.

A biblioteca deve se chamar @minha-org/ui.

Requisitos principais:
- Criar um entry point @minha-org/ui/core.
- Criar um secondary entry point por componente UI.
- Cada componente deve poder ser importado individualmente.
- Todos os componentes devem depender de @minha-org/ui/core.
- Nenhum componente deve importar codigo interno de outro componente.
- Imports entre componentes so podem acontecer via entry point publico.
- A migracao deve ser incremental.
- O app atual deve continuar compilando durante a migracao.
- O primeiro componente migrado deve ser um piloto simples.

Use estes arquivos como referencia:
@sdd-angular-ui-library-example/sdd-angular-ui-library.md
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
1. inventario dos componentes UI existentes
2. criacao da library
3. criacao do core
4. migracao de um componente piloto
5. atualizacao do app consumidor
6. validacao de build/testes
7. migracao incremental dos demais componentes

Nao implemente codigo ainda.
```

Estrutura esperada:

```text
openspec/
  changes/
    extrair-ui-components-para-angular-library/
      proposal.md
      design.md
      tasks.md
      specs/
```

## 3. Revisar a Mudanca Antes de Implementar

No Cursor:

```text
Revise a mudanca OpenSpec criada em:
@openspec/changes/extrair-ui-components-para-angular-library/proposal.md
@openspec/changes/extrair-ui-components-para-angular-library/design.md
@openspec/changes/extrair-ui-components-para-angular-library/tasks.md
@openspec/changes/extrair-ui-components-para-angular-library/specs/

Verifique se:
- o core esta bem definido
- os secondary entry points estao claros
- as tasks estao pequenas o suficiente
- nao ha implementacao grande demais em uma unica task
- o app atual permanece compilavel durante a migracao

Nao implemente ainda. Apenas aponte ajustes necessarios.
```

## 4. Ajustar a Spec Quando Necessario

Use este prompt se a revisao encontrar lacunas:

```text
Atualize a mudanca OpenSpec com estes ajustes:

- O pacote principal @minha-org/ui nao deve exportar todos os componentes.
- Cada componente deve exportar apenas sua API publica via public-api.ts.
- Imports internos entre entry points sao proibidos.
- O primeiro componente piloto deve ser escolhido pelo menor acoplamento.
- A migracao deve parar apos o piloto ate validacao manual.

Atualize proposal.md, design.md, tasks.md e specs conforme necessario.
Nao implemente codigo.
```

## 5. Implementar Somente Depois da Revisao

No Cursor:

```text
/opsx:apply

Implemente apenas a primeira etapa de @openspec/changes/extrair-ui-components-para-angular-library/tasks.md.

Pare apos:
- criar a estrutura da library
- criar o core
- migrar um componente piloto
- rodar build/testes relevantes
- atualizar tasks.md

Nao migre todos os componentes ainda.
```

## 6. Continuar a Migracao em Lotes Pequenos

Depois que o componente piloto estiver validado:

```text
/opsx:apply

Continue a migracao seguindo @openspec/changes/extrair-ui-components-para-angular-library/tasks.md.

Migre apenas o proximo componente listado.
Antes de editar, confirme suas dependencias.
Depois de editar:
- rode build/testes relevantes
- atualize tasks.md
- reporte qualquer ajuste necessario na spec
- pare antes do proximo componente
```

## 7. Arquivar a Mudanca

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

## Regra Principal

Os arquivos deste diretorio sao entrada e referencia.

A fonte oficial da mudanca deve ser gerada e mantida pelo OpenSpec em:

```text
openspec/changes/extrair-ui-components-para-angular-library/
```

O Cursor deve implementar codigo somente depois que `proposal.md`, `design.md`, `tasks.md` e `specs/` estiverem revisados.
