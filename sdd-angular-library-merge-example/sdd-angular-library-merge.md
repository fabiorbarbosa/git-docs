# Spec - Merge de Duas Angular Libraries

## 1. Contexto

O projeto possui duas Angular Libraries que devem ser consolidadas em uma unica library publicavel.

Os componentes, diretivas, pipes e servicos publicos das duas libraries nao conflitam entre si. Os conflitos esperados estao nos arquivos base do Angular, configuracoes de build, empacotamento, TypeScript, testes, estilos base e metadados de pacote.

## 2. Objetivo

Criar uma library final chamada `@minha-org/ui`, consolidando os artefatos publicos das duas libraries originais.

A library final deve:

- preservar componentes e APIs publicas sempre que possivel
- consolidar arquivos base do Angular
- manter build e testes funcionando
- permitir migracao incremental dos consumidores
- reduzir duplicacao de configuracao

## 3. Fora do Escopo

- Redesenhar componentes.
- Renomear componentes sem necessidade.
- Reescrever logica interna sem motivo tecnico.
- Alterar comportamento visual ou funcional.
- Publicar pacote em registry externo nesta primeira etapa.
- Migrar consumidores externos sem plano explicito.

## 4. Inventario Inicial

### Library A

- **Nome atual:**
- **Package name atual:**
- **Caminho:**
- **Entry points:**
- **Exports publicos:**
- **Dependencias:**
- **Estilos/assets:**
- **Testes:**

### Library B

- **Nome atual:**
- **Package name atual:**
- **Caminho:**
- **Entry points:**
- **Exports publicos:**
- **Dependencias:**
- **Estilos/assets:**
- **Testes:**

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF-001 | Definir uma library alvo para consolidacao. | Alta |
| RF-002 | Migrar todos os exports publicos da Library A. | Alta |
| RF-003 | Migrar todos os exports publicos da Library B. | Alta |
| RF-004 | Consolidar arquivos base do Angular e empacotamento. | Alta |
| RF-005 | Preservar componentes sem conflito de nome. | Alta |
| RF-006 | Atualizar paths/imports internos para a nova estrutura. | Alta |
| RF-007 | Manter build da library final funcionando. | Alta |
| RF-008 | Criar estrategia de compatibilidade para consumidores existentes. | Media |

## 6. Requisitos Nao Funcionais

| ID | Categoria | Requisito |
| --- | --- | --- |
| RNF-001 | Build | A library consolidada deve compilar com `ng build`. |
| RNF-002 | Compatibilidade | Dependencias Angular devem ficar em `peerDependencies` quando aplicavel. |
| RNF-003 | Manutencao | Configuracoes duplicadas devem ser removidas ou centralizadas. |
| RNF-004 | Testes | Testes relevantes das duas libraries devem ser preservados. |
| RNF-005 | API publica | Exports publicos devem ser explicitamente revisados antes da remocao de qualquer API. |

## 7. Arquitetura Alvo

Estrutura esperada:

```text
projects/ui/
  package.json
  ng-package.json
  src/
    public-api.ts
    lib/
      library-a/
      library-b/
      shared/
    styles/
    assets/
```

Se as libraries atuais ja usam secondary entry points, preservar essa estrategia:

```text
projects/ui/
  package.json
  ng-package.json
  core/
    ng-package.json
    src/public-api.ts
  component-from-a/
    ng-package.json
    src/public-api.ts
  component-from-b/
    ng-package.json
    src/public-api.ts
```

## 8. Criterio Para Escolher a Library Alvo

Escolha como base a library que tiver:

- configuracao de build mais atual
- maior numero de consumidores
- menor acoplamento com o app principal
- melhor cobertura de testes
- package metadata mais correto
- estrutura mais proxima da arquitetura desejada

Se nenhuma library for claramente melhor, criar uma nova library alvo limpa e migrar ambas para ela.

## 9. Arquivos Base a Consolidar

### `angular.json`

- Manter apenas um projeto de library final.
- Remover builders duplicados depois da migracao.
- Atualizar nomes de projeto e paths.
- Preservar configuracoes de test/build relevantes.

### `tsconfig*.json`

- Consolidar `paths`.
- Remover aliases antigos somente depois que consumidores internos forem migrados.
- Evitar aliases que apontem para arquivos internos.
- Manter compatibilidade temporaria quando necessario.

### `package.json`

- Consolidar scripts.
- Unificar `dependencies`, `peerDependencies` e `devDependencies`.
- Evitar duplicacao de versoes.
- Garantir que `@angular/*` esteja em `peerDependencies` para pacote publicavel quando aplicavel.

### `ng-package.json`

- Definir entry file correto.
- Consolidar assets permitidos.
- Garantir que secondary entry points tenham seus proprios `ng-package.json` quando usados.

### `public-api.ts`

- Exportar somente APIs publicas.
- Evitar exportar arquivos internos.
- Preservar exports existentes com aliases temporarios se necessario.
- Separar exports por entry point quando houver secondary entry points.

### Estilos e Assets

- Consolidar estilos base em uma unica pasta.
- Evitar duplicacao de tokens, variaveis e mixins.
- Preservar caminhos de assets usados pelos componentes.
- Documentar qualquer mudanca de import de CSS/SCSS.

## 10. Regras de Dependencia

Permitido:

```ts
import { ComponentA } from '@minha-org/ui/component-a';
import { ComponentB } from '@minha-org/ui/component-b';
import { UiThemeToken } from '@minha-org/ui/core';
```

Permitido temporariamente durante migracao interna:

```ts
import { ComponentA } from '@old-lib-a/component-a';
```

Proibido na estrutura final:

```ts
import { Something } from '../../old-lib-a/src/internal';
import { SomethingElse } from '../../old-lib-b/src/lib/private';
```

## 11. Estrategia de Compatibilidade

Escolher uma das estrategias:

### Opcao A - Migração Direta

Todos os consumidores internos passam a importar da nova library.

Use quando:

- poucos consumidores usam as libraries antigas
- o projeto consegue alterar imports em uma unica etapa
- nao ha consumidores externos publicados

### Opcao B - Aliases Temporarios

Manter aliases TypeScript temporarios apontando para a nova library.

Use quando:

- ha muitos consumidores internos
- a migracao precisa ser gradual
- ainda existem imports antigos em partes do workspace

### Opcao C - Pacotes Compatibilidade

Manter pacotes antigos como wrappers que reexportam a nova library.

Use quando:

- ha consumidores externos
- nao e possivel quebrar imports publicados
- a migracao precisa de uma janela de deprecacao

## 12. Plano de Migracao Incremental

1. Inventariar Library A e Library B.
2. Comparar exports publicos e dependencias.
3. Escolher library alvo ou criar uma nova.
4. Consolidar configuracoes base sem mover componentes ainda.
5. Migrar um conjunto pequeno de exports da Library A.
6. Rodar build/testes.
7. Migrar um conjunto pequeno de exports da Library B.
8. Rodar build/testes.
9. Atualizar imports internos para a nova library.
10. Remover configuracoes antigas somente quando nao houver consumidores.
11. Documentar APIs preservadas, removidas ou deprecadas.

## 13. Testes

### Testes de Build

- `ng build @minha-org/ui`
- build do app consumidor
- validacao de package final gerado em `dist/`

### Testes Unitarios

- manter testes existentes dos componentes da Library A
- manter testes existentes dos componentes da Library B
- adicionar testes quando componentes migrados nao tiverem cobertura minima

### Testes de Integracao

- consumir componentes migrados no app atual
- validar imports via nova API publica
- validar estilos/assets em runtime quando aplicavel

### Testes de Contrato Publico

- comparar exports antes e depois da migracao
- garantir que APIs removidas estejam documentadas
- validar aliases/wrappers quando usados

## 14. Criterios de Aceite

- A library final compila com sucesso.
- Os componentes das duas libraries estao acessiveis pela nova API publica.
- Arquivos base duplicados foram consolidados.
- Nao existem imports finais apontando para arquivos internos das libraries antigas.
- O app consumidor compila usando a nova library.
- Testes relevantes das duas libraries passam.
- Estrategia de compatibilidade esta documentada.
- Libraries antigas so sao removidas depois que nao houver imports ativos.

## 15. Riscos

| Risco | Impacto | Mitigacao |
| --- | --- | --- |
| Quebra de imports existentes | Alto | Usar aliases temporarios ou wrappers de compatibilidade. |
| Perda de exports publicos | Alto | Gerar inventario antes/depois dos public-api.ts. |
| Configuracoes Angular conflitantes | Medio | Escolher uma library alvo e migrar configuracoes de forma controlada. |
| Duplicacao de estilos base | Medio | Consolidar tokens/mixins e validar visualmente componentes criticos. |
| Remocao prematura das libraries antigas | Alto | Remover somente depois de busca global por imports antigos. |

## 16. Rollback

Se uma etapa falhar:

1. Reverter somente a etapa atual.
2. Manter inventario e decisoes documentadas.
3. Restaurar imports antigos do consumidor afetado.
4. Corrigir configuracao ou API antes de tentar novamente.
5. Nao remover libraries antigas ate o final da validacao.

## 17. Tasks

- [ ] Inventariar Library A.
- [ ] Inventariar Library B.
- [ ] Listar todos os `public-api.ts` e exports publicos.
- [ ] Listar todos os entry points e secondary entry points.
- [ ] Comparar dependencias e peerDependencies.
- [ ] Comparar configuracoes Angular, TypeScript, teste e build.
- [ ] Escolher a library alvo ou criar uma nova library limpa.
- [ ] Consolidar `angular.json`.
- [ ] Consolidar `tsconfig*.json`.
- [ ] Consolidar `package.json`.
- [ ] Consolidar `ng-package.json`.
- [ ] Consolidar estilos base e assets.
- [ ] Migrar primeiro lote pequeno da Library A.
- [ ] Validar build/testes.
- [ ] Migrar primeiro lote pequeno da Library B.
- [ ] Validar build/testes.
- [ ] Atualizar imports internos para a nova library.
- [ ] Criar aliases ou wrappers temporarios se necessario.
- [ ] Remover configuracoes antigas sem consumidores ativos.
- [ ] Documentar estrategia de consumo final.

## 18. Definition of Done

- Library consolidada criada e compilando.
- Componentes das duas libraries disponiveis na nova API publica.
- Configuracoes base duplicadas consolidadas.
- Imports internos proibidos removidos.
- Consumidor principal compilando.
- Testes relevantes passando.
- Compatibilidade ou breaking changes documentados.
- Libraries antigas removidas ou marcadas como deprecated com plano claro.
