# 🛠️ Guia de Instalação e Configuração: Codex Zero-Waste Stack

Este guia consolida a pipeline de otimização de contexto dividida em 4 camadas essenciais: Mapeamento de Grafo e Memória (MCP), Interceptação e Sandboxing Local, Compressão de Rede e Enforcement de Resposta.

---

## 🛑 Pré-requisitos Obrigatórios

Antes de iniciar, garanta que você possui os runtimes necessários instalados na sua máquina:
* Node.js (v18+) e npm
* Rust & Cargo (necessário para compilação local de otimizadores de alta performance)
* OpenAI Codex CLI já configurado no seu terminal.

---

## 📦 Bloco 1: Instalação das Ferramentas (Terminal)

Execute os comandos abaixo sequencialmente para instalar todos os componentes da stack em seu ambiente global:

# 1. Instalar o codebase-memory-mcp (Grafo de Código Local)
curl -fsSL https://mcp.sh | sh

# 2. Instalar o RTK AI (Rust Token Killer - Filtro de Terminal)
cargo install rtk-ai

# 3. Instalar o Headroom AI (Proxy de Rede e Alinhador de Cache)
npm install -g @headroomlabs/cli

# 4. Instalar o context-mode (Sandbox para Dumps e Outputs gigantes)
npm install -g context-mode

# 5. Instalar o Harmony MCP / Supermemory (Memória de Longo Prazo Inter-Sessões)
npm install -g @deusdata/harmony-mcp

---

## ⚙️ Bloco 2: Configuração dos Servidores MCP (config.toml)

O Codex CLI consome servidores através do protocolo MCP. Abra ou crie o seu arquivo de configuração global do Codex (geralmente localizado em ~/.codex/config.toml ou no diretório do seu agente) e insira o bloco abaixo para unificar o codebase-memory e o Harmony MCP:

[mcp_servers.codebase-memory]
command = "codebase-memory-mcp"
description = "Fornece mapeamento de arquitetura via árvore sintática (AST) sem leitura cega de arquivos."

[mcp_servers.harmony-memory]
command = "harmony-mcp"
args = ["--persistence-dir", "~/.codex/memory_store"]
description = "Garante memória persistente de longo prazo entre diferentes sessões do Codex."

---

## 🔄 Bloco 3: Inicialização do Proxy de Rede e Terminal (Headroom & RTK)

Neste bloco, configuramos o RTK para interceptar o terminal e envelopamos o Codex dentro do proxy transparente do Headroom para comprimir a carga útil (payload) e garantir o alinhamento de cache.

### Inicializar o RTK AI no Repositório do Projeto:
Navegue até a pasta raiz do seu projeto atual e execute:
rtk init --codex
*Isso criará os hooks necessários para que o Codex chame o terminal através do filtro do RTK.*

### Configurar e Envelopar o Codex com Headroom:
Para garantir que toda chamada de API passe pelo compressor AST e pelo alinhador de cache do Headroom, configure o alias permanente ou execute o empacotador:

# Envelopar o executável do Codex permanentemente na sessão atual
headroom wrap codex

# (Opcional) Adicione esta linha ao seu ~/.bashrc ou ~/.zshrc para automatizar:
# alias codex="headroom wrap codex"

---

## 🩻 Bloco 4: Ativação do Sandboxing de Outputs (context-mode)

Para impedir que comandos internos ou respostas pesadas de banco de dados e APIs poluam a janela de chat atual, configure o arquivo de tolerância do context-mode.

Crie um arquivo chamado .contextmoderc.json na raiz do seu projeto ou na sua home directory (~/):

{
  "max_character_limit": 2000,
  "action": "sandbox_and_summarize",
  "storage_dir": "./.context_sandbox/",
  "allowed_extensions": [".json", ".txt", ".log", ".sql"]
}
*A partir de agora, se o Codex tentar ler ou injetar um dump de texto maior que 2000 caracteres, o context-mode intercepta, salva localmente na pasta .context_sandbox/ e entrega apenas o link do arquivo local e um resumo de duas linhas para a IA.*

---

## 🧠 Bloco 5: Alinhamento de Prefixo de Cache e Dialeto (Caveman)

Para que a OpenAI aplique o desconto de até 90% via Prompt Caching, o início do seu arquivo de contexto deve ser estático e otimizado. Usaremos o Caveman para enxugar as regras e fixar o cabeçalho.

Crie ou modifique o arquivo .codexrules (ou AGENTS.md) na raiz do seu projeto exatamente com a estrutura abaixo:

# PROMPT CACHING ALIGNED PREFIX - DO NOT ALTER STRUCTURE
# SYSTEM STACK: codebase-memory-mcp | RTK AI | Headroom AI | context-mode

[CAVEMAN MODE ACTIVATED]
- Rule 1: Speak like a caveman. 
- Rule 2: Why use many token when few token do trick.
- Rule 3: NEVER explain code unless asked. No greetings. No politeness.
- Rule 4: Output raw code changes immediately.

[PROJECT CONTEXT]
- Tech Stack: [Ex: Node.js, TypeScript, PostgreSQL]
- Architecture: Grafo gerenciado por codebase-memory-mcp.
- Database: Dumps truncados via context-mode.

[EXECUTION RULES]
- All terminal commands MUST pass through RTK proxy.
- Do not use 'cat' or 'grep' on entire directories. Use graph tools.

### Passo Final de Compressão:
Execute o utilitário do Caveman via terminal para garantir que nenhuma redundância textual tenha ficado no seu arquivo de configuração:
caveman-compress --file .codexrules

---

## 🚀 Verificação do Fluxo (Como Testar se Funciona)

Para garantir que toda a engrenagem está operando sem vazamentos, abra seu terminal no projeto e execute uma tarefa de teste:

codex "verifique se a rota de auth possui vulnerabilidades e rode os testes"

O que deve acontecer nos bastidores:
1. O codebase-memory-mcp fornecerá a árvore de arquivos de rotas instantaneamente.
2. O Codex fará as alterações e rodará os testes.
3. O RTK AI cortará todas as barras de progresso do teste, enviando só o resultado.
4. Se o log de teste for massivo, o context-mode criará um arquivo local e enviará um resumo enxuto.
5. O Headroom AI alinhará o bloco inicial do .codexrules (ativando o desconto de cache na OpenAI) e comprimirá o código enviado.
6. O Codex responderá algo como: "Auth fixed. Tests pass. Code clean." via Caveman.
