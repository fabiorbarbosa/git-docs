# Prompt Cursor + OpenSpec

Use este prompt no Cursor para iniciar uma mudanca OpenSpec voltada a extracao de componentes UI Angular para uma biblioteca reutilizavel.

```text
/opsx:new extrair-ui-components-para-angular-library

Quero extrair todos os componentes de UI deste projeto Angular para uma nova biblioteca Angular publicavel.

Objetivo:
Criar uma biblioteca chamada @minha-org/ui, onde:
- @minha-org/ui/core contem tokens, temas, estilos base, utilitarios, servicos compartilhados, diretivas base e contratos comuns.
- Cada componente UI deve ser exposto por um secondary entry point individual.
- O consumidor deve importar componentes individualmente, por exemplo:
  import { UiButtonComponent } from '@minha-org/ui/button';
  import { UiInputComponent } from '@minha-org/ui/input';
- Todos os componentes devem depender de @minha-org/ui/core.
- Nenhum componente deve importar codigo interno de outro componente, exceto via entry point publico quando for uma dependencia explicita.
- A biblioteca deve preservar comportamento visual e funcional atual.
- A migracao deve ser incremental, sem quebrar o app existente.

Antes de implementar, gere proposal.md, design.md, specs e tasks.md.

Use o template docs/spec-templates/spec-driven-development-angular.md como checklist obrigatorio.

Inclua no design:
- estrutura de pastas da library
- estrategia de secondary entry points
- estrategia de dependencias com core
- convencao de nomes
- regras de public-api.ts
- estrategia de theming/design tokens
- estrategia de testes
- plano de migracao dos imports no app atual
- criterio para decidir se algo vai para core ou para um componente
- riscos e rollback

Nao implemente ainda. Primeiro gere a spec e aguarde revisao.
```

## Prompt de Implementacao Apos Revisao

Use somente depois que `proposal.md`, `design.md`, `specs/` e `tasks.md` estiverem revisados.

```text
/opsx:apply

Implemente apenas as tasks aprovadas em @openspec/changes/extrair-ui-components-para-angular-library/tasks.md.

Comece pelo core e por um componente piloto simples.
Nao migre todos os componentes de uma vez.

Depois de cada etapa:
- atualize tasks.md
- rode build/testes relevantes
- reporte arquivos alterados
- pare antes da proxima leva de componentes
```

## Referencias Locais Recomendadas

Ao usar no Cursor, referencie tambem:

```text
@docs/spec-templates/spec-driven-development-angular.md
@openspec/changes/extrair-ui-components-para-angular-library/tasks.md
@openspec/changes/extrair-ui-components-para-angular-library/design.md
@openspec/changes/extrair-ui-components-para-angular-library/specs/
```
