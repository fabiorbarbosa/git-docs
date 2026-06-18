# Spec - Extrair UI Components para Angular Library

## 1. Contexto

O projeto Angular atual possui componentes de UI acoplados ao app principal. Queremos extrair esses componentes para uma biblioteca reutilizavel, publicavel e consumivel por outros projetos Angular.

A biblioteca deve permitir consumo individual por componente, mantendo uma dependencia comum em um pacote core.

## 2. Objetivo

Criar a biblioteca `@minha-org/ui` com entry points individuais:

- `@minha-org/ui/core`
- `@minha-org/ui/button`
- `@minha-org/ui/input`
- `@minha-org/ui/select`
- `@minha-org/ui/modal`
- `@minha-org/ui/table`

Cada componente deve ser importavel de forma isolada e depender apenas do `core` e de suas dependencias publicas explicitas.

## 3. Fora do Escopo

- Redesenhar visual dos componentes.
- Trocar framework CSS.
- Criar novo design system completo.
- Publicar pacote em registry externo nesta primeira etapa.
- Reescrever componentes sem necessidade funcional.

## 4. Requisitos Funcionais

| ID | Requisito | Prioridade |
| --- | --- | --- |
| RF-001 | Criar library Angular publicavel `@minha-org/ui`. | Alta |
| RF-002 | Criar entry point `@minha-org/ui/core`. | Alta |
| RF-003 | Criar um entry point por componente UI. | Alta |
| RF-004 | Cada componente deve importar contratos compartilhados de `@minha-org/ui/core`. | Alta |
| RF-005 | O app atual deve continuar funcionando apos migracao incremental. | Alta |
| RF-006 | Componentes devem manter API publica compativel sempre que possivel. | Media |

## 5. Requisitos Nao Funcionais

| ID | Categoria | Requisito |
| --- | --- | --- |
| RNF-001 | Build | A library deve compilar com `ng build`. |
| RNF-002 | Tree shaking | Consumidores devem conseguir importar apenas componentes usados. |
| RNF-003 | Manutencao | Nenhum import deve apontar para arquivos internos de outro entry point. |
| RNF-004 | Compatibilidade | Dependencias Angular devem ser `peerDependencies`. |
| RNF-005 | Testes | Componentes migrados devem manter ou ganhar testes unitarios. |

## 6. Arquitetura Proposta

Estrutura esperada:

```text
projects/ui/
  package.json
  ng-package.json
  core/
    ng-package.json
    src/
      public-api.ts
      tokens/
      theme/
      directives/
      services/
      types/
  button/
    ng-package.json
    src/
      public-api.ts
      button.component.ts
      button.component.html
      button.component.scss
      button.component.spec.ts
  input/
    ng-package.json
    src/
      public-api.ts
      input.component.ts
      input.component.html
      input.component.scss
      input.component.spec.ts
```

## 7. Regra de Dependencia

Permitido:

```ts
import { UiThemeService } from '@minha-org/ui/core';
```

Permitido quando explicitamente necessario:

```ts
import { UiIconComponent } from '@minha-org/ui/icon';
```

Proibido:

```ts
import { UiThemeService } from '../../core/src/services/theme.service';
import { Something } from '../input/src/internal';
```

## 8. Definicao do Core

Vai para `@minha-org/ui/core` quando for:

- design token
- tema
- configuracao global
- servico compartilhado
- diretiva base
- tipo ou interface publica
- utilitario usado por mais de um componente
- provider comum da biblioteca

Nao vai para `core` quando for:

- logica especifica de um componente
- template de componente
- estilo especifico de componente
- dependencia usada por apenas um componente

## 9. API Publica Esperada

Exemplo de consumo:

```ts
import { UiButtonComponent } from '@minha-org/ui/button';
import { UiInputComponent } from '@minha-org/ui/input';
import { provideUiCore } from '@minha-org/ui/core';
```

Exemplo de bootstrap:

```ts
bootstrapApplication(AppComponent, {
  providers: [
    provideUiCore({
      theme: 'default'
    })
  ]
});
```

## 10. Contrato de Empacotamento

### Package principal

O pacote principal `@minha-org/ui` deve existir apenas como raiz de empacotamento e documentacao. Exports amplos devem ser evitados para nao incentivar imports agregados.

### Entry point core

`@minha-org/ui/core` deve exportar somente APIs estaveis:

- providers
- tokens
- tipos
- diretivas base
- servicos compartilhados
- helpers publicos

### Entry points de componentes

Cada componente deve possuir:

- `ng-package.json`
- `src/public-api.ts`
- componente standalone ou modulo publico, conforme padrao do projeto
- testes
- estilos encapsulados ou referenciando tokens do core

## 11. Convencoes de Nome

- Prefixo de componentes: `Ui`.
- Arquivos em kebab-case.
- Classes em PascalCase.
- Entry points em kebab-case.
- Exports publicos sempre via `public-api.ts`.

Exemplos:

```ts
UiButtonComponent
UiInputComponent
UiModalComponent
```

## 12. Estrategia de Migracao Incremental

1. Criar library vazia.
2. Criar `core`.
3. Migrar design tokens e providers.
4. Escolher componente simples como piloto, por exemplo `button`.
5. Validar build, teste e consumo no app atual.
6. Migrar componentes restantes por ordem de dependencia.
7. Atualizar imports do app.
8. Remover componentes duplicados do app original.

## 13. Ordem Recomendada de Migracao

1. `core`
2. `icon`
3. `button`
4. `input`
5. `select`
6. `checkbox`
7. `radio`
8. `modal`
9. `table`
10. componentes compostos

## 14. Testes

### Testes Unitarios

- Renderizacao basica de cada componente.
- Inputs obrigatorios e opcionais.
- Outputs/eventos.
- Classes CSS relevantes.
- Estados disabled, loading, error e active quando existirem.

### Testes de Integracao

- Consumo de componente no app atual.
- Uso do provider `provideUiCore`.
- Interacao entre componente e tema.

### Testes de Build

- `ng build @minha-org/ui`
- build do app consumidor
- validacao de imports via entry points publicos

## 15. Criterios de Aceite

- `ng build @minha-org/ui` executa com sucesso.
- Cada componente possui seu proprio entry point.
- `@minha-org/ui/core` e usado como dependencia comum.
- O app atual compila consumindo ao menos um componente via novo entry point.
- Nao existem imports internos entre entry points.
- Componentes migrados mantem comportamento visual e funcional.
- Testes dos componentes migrados passam.

## 16. Riscos

| Risco | Impacto | Mitigacao |
| --- | --- | --- |
| Componentes muito acoplados ao app atual | Alto | Migrar primeiro dependencias compartilhadas para `core` e escolher piloto simples. |
| Imports internos entre entry points | Alto | Criar regra de lint ou revisao obrigatoria por import publico. |
| Quebra visual apos migracao | Medio | Comparar componente antigo e novo em tela de showcase ou app consumidor. |
| API publica instavel | Medio | Definir exports minimos e documentar breaking changes. |
| Migracao grande demais | Alto | Migrar por lotes pequenos e manter app funcionando. |

## 17. Rollback

Se a migracao de um componente falhar:

1. Reverter apenas o consumo do componente no app atual.
2. Manter o entry point criado se ele nao quebrar build.
3. Registrar o problema em `tasks.md`.
4. Corrigir dependencias ou API antes de tentar nova migracao.

## 18. Tasks

- [ ] Inventariar todos os componentes UI existentes.
- [ ] Classificar componentes por complexidade e dependencias.
- [ ] Criar projeto de library Angular.
- [ ] Criar entry point `core`.
- [ ] Migrar tokens, tema, tipos e providers para `core`.
- [ ] Criar testes do `core`.
- [ ] Criar entry point para primeiro componente piloto.
- [ ] Migrar componente piloto.
- [ ] Ajustar imports do componente piloto para usar `@minha-org/ui/core`.
- [ ] Criar testes do componente piloto.
- [ ] Validar build da library.
- [ ] Migrar app atual para consumir componente piloto.
- [ ] Validar build/testes do app atual.
- [ ] Repetir migracao por componente.
- [ ] Remover exports antigos quando a migracao estiver completa.
- [ ] Documentar exemplos de uso.

## 19. Definition of Done

- Library criada e compilando.
- `core` criado e consumido pelos componentes migrados.
- Pelo menos um componente piloto publicado como secondary entry point.
- App atual consumindo o componente piloto pela nova API publica.
- Sem imports internos proibidos.
- Testes relevantes passando.
- Documentacao de uso atualizada.
