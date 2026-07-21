# Guia de Migração: Angular 14 para 18 + Configuração do Tailwind CSS

Este guia contém o passo a passo seguro para atualizar sua aplicação do Angular 14 para o Angular 18 e configurar a versão mais recente do Tailwind CSS utilizando o novo motor de build do Angular.

---

## Parte 1: Migração do Angular (Versão por Versão)

O Angular não permite pular versões principais diretamente. Você deve atualizar uma versão por vez para garantir que os scripts de migração automática funcionem.

### Pré-requisitos
1. **Backup:** Faça um commit ou crie uma nova branch antes de iniciar.
2. **Node.js:** Atualize o Node.js para a **versão 18.19.1+ ou versão 20** (altamente recomendada para o Angular 18).

### Execução dos Comandos
Execute os comandos abaixo sequencialmente na raiz do projeto. **Dica:** Teste e rode a aplicação (`ng serve`) após a conclusão de cada passo.

#### 1. Angular 14 ➔ Angular 15
```bash
ng update @angular/core@15 @angular/cli@15
# Se usar Angular Material:
ng update @angular/material@15
```

#### 2. Angular 15 ➔ Angular 16
```bash
ng update @angular/core@16 @angular/cli@16
# Se usar Angular Material:
ng update @angular/material@16
```

#### 3. Angular 16 ➔ Angular 17
```bash
ng update @angular/core@17 @angular/cli@17
# Se usar Angular Material:
ng update @angular/material@17
```

#### 4. Angular 17 ➔ Angular 18
```bash
ng update @angular/core@18 @angular/cli@18
# Se usar Angular Material:
ng update @angular/material@18
```
*Nota: Ao atualizar para a v18, o CLI perguntará se deseja migrar para o novo **Application Builder (Vite/ESBuild)**. Aceite para obter builds muito mais rápidos.*

> **Nota sobre erros:** Se alguma biblioteca de terceiros bloquear a atualização devido a conflitos de versão, você pode forçar o comando adicionando a flag `--force` no final do comando (ex: `ng update @angular/core@15 @angular/cli@15 --force`).

---

## Parte 2: Configuração do Tailwind CSS no Angular 18

Com o novo compilador do Angular 18, o processo ficou simplificado e não exige arquivos extras de configuração do PostCSS.

### 1. Instalar as dependências do Tailwind
Instale o Tailwind CSS e seus pacotes necessários como dependências de desenvolvimento:
```bash
npm install -D tailwindcss postcss autoprefixer
```

### 2. Inicializar o arquivo de configuração
Gere o arquivo de configuração padrão do Tailwind:
```bash
npx tailwindcss init
```

### 3. Configurar os caminhos dos templates
Abra o arquivo `tailwind.config.js` criado na raiz do seu projeto e adicione o caminho dos arquivos do Angular na propriedade `content`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 4. Adicionar as diretivas ao CSS Global
Abra o arquivo de estilos globais do seu app (geralmente `src/styles.css` ou `src/styles.scss`) e adicione as três diretivas do Tailwind no topo do arquivo:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

---

## Pronto!
Agora você pode rodar o seu servidor de desenvolvimento:
```bash
ng serve
```
O Angular 18 detectará automaticamente o seu arquivo `tailwind.config.js` e aplicará as classes utilitárias instantaneamente nos seus componentes.
